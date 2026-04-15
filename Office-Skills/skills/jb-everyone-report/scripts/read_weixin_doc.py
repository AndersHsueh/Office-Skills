#!/usr/bin/env python3
"""
读取企业微信在线文档（表格）内容的工具脚本
依赖：pycryptodome, playwright-cli（命令行工具）

用法:
  python3 read_weixin_doc.py --url <文档URL> [--output <输出文件>] [--tab <Sheet名>]
  python3 read_weixin_doc.py  # 使用默认配置

示例:
  python3 read_weixin_doc.py --url "https://doc.weixin.qq.com/sheet/e3_AT8ADwZoAGgCNTrZqBm7TQGy3wNRD?scode=xxx" --output 金碧工时.tsv
"""

import sys
import os
import sqlite3
import subprocess
import json
import time
import argparse
import csv
from io import StringIO
from pathlib import Path

# pycryptodome 可能安装在用户目录
USER_SITE = os.path.expanduser("~/.local/lib/python3.13/site-packages")
if USER_SITE not in sys.path:
    sys.path.insert(0, USER_SITE)

try:
    from Crypto.Cipher import AES
    from hashlib import pbkdf2_hmac
except ImportError:
    print("❌ 需要安装 pycryptodome: pip install pycryptodome")
    sys.exit(1)

# ─────────────────────────────────────────────
# Cookie 提取与解密
# ─────────────────────────────────────────────

def get_chrome_key() -> bytes:
    """从 macOS Keychain 获取 Chrome 加密密钥"""
    result = subprocess.run(
        ["security", "find-generic-password", "-w", "-s", "Chrome Safe Storage"],
        capture_output=True, text=True, check=True
    )
    password = result.stdout.strip()
    return pbkdf2_hmac("sha1", password.encode(), b"saltysalt", 1003, dklen=16)


def decrypt_cookie(encrypted_value: bytes, key: bytes) -> str:
    """解密 Chrome Cookie（macOS v10 格式）"""
    if encrypted_value[:3] == b"v10":
        iv = b" " * 16
        decrypted = AES.new(key, AES.MODE_CBC, IV=iv).decrypt(encrypted_value[3:])
        padding = decrypted[-1]
        if padding <= 16:
            decrypted = decrypted[:-padding]
        text = decrypted.decode("utf-8", errors="replace")
        # 实际值在 _ 分隔符之后
        return text.split("_", 1)[1] if "_" in text else text
    return encrypted_value.decode("utf-8", errors="replace")


def get_weixin_cookies(domain: str = ".doc.weixin.qq.com") -> dict:
    """获取指定域名的所有解密后 Cookie"""
    key = get_chrome_key()
    db_path = os.path.expanduser(
        "~/Library/Application Support/Google/Chrome/Default/Cookies"
    )
    conn = sqlite3.connect(db_path)
    cookies = {}
    rows = conn.execute(
        "SELECT name, encrypted_value FROM cookies WHERE host_key LIKE ?",
        (f"%{domain.lstrip('.')}%",),
    ).fetchall()
    conn.close()
    for name, enc_val in rows:
        val = decrypt_cookie(enc_val, key)
        if val and all(ord(c) < 128 for c in val):
            cookies[name] = val
    return cookies


def cookies_to_string(cookies: dict) -> str:
    return "; ".join(f"{k}={v}" for k, v in cookies.items())

# ─────────────────────────────────────────────
# Playwright CLI 操作
# ─────────────────────────────────────────────

def run_pw(cmd: str, timeout: int = 30) -> str:
    """执行 playwright-cli 命令，返回输出"""
    result = subprocess.run(
        f"playwright-cli {cmd}",
        shell=True, capture_output=True, text=True, timeout=timeout
    )
    return result.stdout + result.stderr


def inject_cookies_js(cookies: dict) -> str:
    """生成注入 Cookie 的 JS 代码"""
    cookie_list = [
        {"name": k, "value": v, "domain": "doc.weixin.qq.com", "path": "/"}
        for k, v in cookies.items()
    ]
    return json.dumps(cookie_list)


# ─────────────────────────────────────────────
# 主流程
# ─────────────────────────────────────────────

COPY_INTERCEPT_JS = """async page => {
  // 拦截 copy 事件来捕获剪贴板数据
  await page.evaluate(() => {
    window.__capturedClipboard = null;
    document.addEventListener('copy', (e) => {
      const d = e.clipboardData.getData('text/plain');
      window.__capturedClipboard = d;
    }, true);
  });
  // 点击画布获取焦点
  await page.click('canvas', { timeout: 5000 }).catch(() => {});
  await page.waitForTimeout(500);
  // 全选 + 复制
  await page.keyboard.press('Meta+a');
  await page.waitForTimeout(500);
  await page.keyboard.press('Meta+c');
  await page.waitForTimeout(2000);
  // 先尝试 copy 事件拦截的数据
  const data = await page.evaluate(() => window.__capturedClipboard);
  if (data) {
    return data;
  }
  // 备选：grantPermissions 后读取 navigator.clipboard
  try {
    await page.context().grantPermissions(['clipboard-read', 'clipboard-write']);
    const text = await page.evaluate(async () => {
      if (navigator.clipboard && navigator.clipboard.readText) {
        return await navigator.clipboard.readText();
      }
      return null;
    });
    return text || 'NO_DATA';
  } catch(e) {
    return 'ERROR: ' + e.message;
  }
}"""


def run_pw_code(js: str, timeout: int = 30) -> str:
    """执行 playwright-cli run-code，返回 Result 内容"""
    tmp = "/tmp/weixin_pw_code.js"
    with open(tmp, "w") as f:
        f.write(js)
    result = subprocess.run(
        f'playwright-cli run-code "$(cat {tmp})"',
        shell=True, capture_output=True, text=True, timeout=timeout
    )
    output = result.stdout
    if "### Result" in output:
        content = output.split("### Result")[1]
        if "### Ran Playwright" in content:
            content = content.split("### Ran Playwright")[0]
        content = content.strip()
        if content.startswith('"') and content.endswith('"'):
            content = content[1:-1]
        return content.replace("\\t", "\t").replace("\\n", "\n").replace('\\"', '"')
    return ""


def read_sheet(url: str, wait_seconds: int = 6) -> str:
    """
    打开企业微信文档并读取全部表格内容（TSV 格式）
    返回 TSV 字符串
    """
    print(f"📖 正在读取文档: {url[:80]}...")

    # 1. 获取 Cookie
    print("🔑 提取 Chrome Cookie...")
    cookies = get_weixin_cookies()
    if not cookies:
        raise RuntimeError("未找到 doc.weixin.qq.com 的 Cookie，请先在 Chrome 中登录企业微信文档")
    print(f"   找到 {len(cookies)} 个 Cookie: {', '.join(cookies.keys())}")

    # 2. 启动浏览器并打开页面
    print("🌐 启动浏览器...")
    run_pw("session-stop-all")
    run_pw("config --browser=chrome")
    run_pw(f'open "{url}"')
    time.sleep(2)

    # 3. 注入 Cookie（单独步骤）
    print("🍪 注入认证 Cookie...")
    cookie_list = json.dumps([
        {"name": k, "value": v, "domain": "doc.weixin.qq.com", "path": "/"}
        for k, v in cookies.items()
    ])
    inject_js = f"async page => {{ await page.context().addCookies({cookie_list}); return 'ok'; }}"
    run_pw_code(inject_js)

    # 4. 刷新页面并等待加载
    print("🔄 刷新页面，等待加载...")
    run_pw("reload")
    time.sleep(wait_seconds)

    # 5. 验证登录
    snapshot = run_pw("snapshot")
    if "企业身份登录" in snapshot or "Scan the QR code" in snapshot:
        raise RuntimeError("登录失败，Cookie 可能已过期，请重新在 Chrome 中访问该文档")
    print("✅ 登录成功！")

    # 6. 拦截 copy 事件并读取数据
    print("📋 读取表格数据...")
    content = run_pw_code(COPY_INTERCEPT_JS, timeout=30)

    if not content or content == "NO_DATA":
        raise RuntimeError("未获取到数据，可能需要更长加载时间，请用 --wait 参数增加等待秒数")

    print("✅ 数据读取成功！")
    return content


def tsv_to_rows(tsv: str) -> list:
    """将 TSV 字符串转换为二维数组"""
    reader = csv.reader(StringIO(tsv), delimiter="\t")
    return list(reader)


def save_output(content: str, output_path: str):
    """保存内容到文件"""
    Path(output_path).write_text(content, encoding="utf-8")
    print(f"💾 已保存到: {output_path}")


def print_preview(rows: list, max_rows: int = 10):
    """打印表格预览"""
    print(f"\n📊 表格预览（共 {len(rows)} 行）：")
    print("-" * 80)
    for i, row in enumerate(rows[:max_rows]):
        # 截断长内容
        cells = [c[:30].replace("\n", "↵") for c in row[:8]]
        print(f"  行{i+1:3d}: {' | '.join(cells)}")
    if len(rows) > max_rows:
        print(f"  ... (还有 {len(rows) - max_rows} 行)")
    print("-" * 80)


# ─────────────────────────────────────────────
# CLI 入口
# ─────────────────────────────────────────────

DEFAULT_URL = (
    "https://doc.weixin.qq.com/sheet/e3_AT8ADwZoAGgCNTrZqBm7TQGy3wNRD"
    "?scode=AP0AqQfLAAojyki8bcAc4AdgZHADI&tab=000001"
)


def main():
    parser = argparse.ArgumentParser(description="读取企业微信在线文档内容")
    parser.add_argument("--url", default=DEFAULT_URL, help="文档 URL")
    parser.add_argument("--output", default=None, help="输出文件路径（默认打印预览）")
    parser.add_argument("--wait", type=int, default=5, help="等待页面加载秒数（默认 5）")
    args = parser.parse_args()

    try:
        tsv_content = read_sheet(args.url, wait_seconds=args.wait)

        if tsv_content.startswith("ERROR:"):
            print(f"❌ {tsv_content}")
            sys.exit(1)

        rows = tsv_to_rows(tsv_content)
        print_preview(rows)

        if args.output:
            save_output(tsv_content, args.output)
        else:
            # 默认保存到当前目录
            default_out = "weixin_doc_output.tsv"
            save_output(tsv_content, default_out)

    except KeyboardInterrupt:
        print("\n已取消")
    except Exception as e:
        print(f"❌ 错误: {e}")
        raise
    finally:
        run_pw("session-stop")


if __name__ == "__main__":
    main()
