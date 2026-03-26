#!/usr/bin/env python3
"""
apifox-bug-finder: 检测系统中 Apifox 恶意域名 apifox.it.com 的痕迹
支持: macOS, Linux, Windows (Git Bash / WSL / CMD / PowerShell)
"""

import os
import sys
import platform
import subprocess
import json
from pathlib import Path

MALICIOUS_DOMAIN = "apifox.it.com"
APIFOX_APP_NAME = "apifox"


def get_os():
    s = platform.system().lower()
    if s == "darwin":
        return "macos"
    elif s == "linux":
        return "linux"
    elif s == "windows" or os.name == "nt":
        return "windows"
    return s


def run_cmd(cmd, shell=True):
    try:
        if isinstance(cmd, list):
            result = subprocess.run(cmd, shell=shell, capture_output=True, text=True)
        else:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout.strip(), result.returncode == 0
    except Exception:
        return "", False


def expand_path(path):
    return os.path.expandvars(os.path.expanduser(path))


def check_nwstate_macos():
    """macOS: 检查 Chromium 系的 Network Persistent State"""
    results = []
    base = Path(expand_path("~/Library/Application Support"))
    if not base.exists():
        return results
    for p in base.rglob("Network Persistent State"):
        try:
            out, ok = run_cmd(f"strings '{p}' | grep -i '{MALICIOUS_DOMAIN}' 2>/dev/null || true")
            if MALICIOUS_DOMAIN in out.lower():
                results.append({"file": str(p), "status": "INFECTED", "detail": "发现恶意域名记录"})
            else:
                results.append({"file": str(p), "status": "CLEAN", "detail": "无恶意域名"})
        except Exception:
            pass
    return results


def check_nwstate_linux():
    """Linux: 检查 Chromium 系的 Network Persistent State"""
    results = []
    paths_to_check = [
        expand_path("~/.config"),
        expand_path("~/.config/chromium"),
        expand_path("~/.config/google-chrome"),
        expand_path("~/.config/brave"),
        expand_path("~/.config/vivaldi"),
    ]
    for base in paths_to_check:
        p = Path(base) / "Network Persistent State"
        if p.exists():
            out, _ = run_cmd(f"strings '{p}' | grep -i '{MALICIOUS_DOMAIN}' 2>/dev/null || true")
            if MALICIOUS_DOMAIN in out.lower():
                results.append({"file": str(p), "status": "INFECTED", "detail": "发现恶意域名记录"})
            else:
                results.append({"file": str(p), "status": "CLEAN", "detail": "无恶意域名"})
    return results


def check_nwstate_windows():
    """Windows: 检查 Chromium 系的 Network Persistent State"""
    results = []
    paths_to_check = [
        os.path.join(os.environ.get("APPDATA", ""), APIFOX_APP_NAME),
        os.path.join(os.environ.get("LOCALAPPDATA", ""), APIFOX_APP_NAME),
        os.path.join(os.environ.get("APPDATA", ""), "ApiFox"),
        os.path.join(os.environ.get("LOCALAPPDATA", ""), "ApiFox"),
    ]
    for base in paths_to_check:
        if not base or not Path(base).exists():
            continue
        # 递归搜索 Network Persistent State
        out, _ = run_cmd(f'dir /S /B "{base}\\*Network Persistent State*" 2>NUL || echo ""')
        for line in out.splitlines():
            line = line.strip()
            if not line or "Network Persistent State" not in line:
                continue
            content, _ = run_cmd(f'type "{line}" 2>NUL || cat "{line}" 2>/dev/null || echo ""')
            if MALICIOUS_DOMAIN.lower() in content.lower():
                results.append({"file": line, "status": "INFECTED", "detail": "发现恶意域名记录"})
            else:
                results.append({"file": line, "status": "CLEAN", "detail": "无恶意域名"})
    return results


def check_apifox_installed_macos():
    """检查 macOS 上是否安装过 Apifox"""
    paths = [
        expand_path("~/Library/Application Support/apifox"),
        expand_path("~/.config/apifox"),
        expand_path("~/Library/Caches/apifox"),
        "/Applications/Apifox.app",
        "/Applications/ApiFox.app",
    ]
    installed = []
    for p in paths:
        if Path(p).exists():
            installed.append(p)
    return installed


def check_apifox_installed_linux():
    """检查 Linux 上是否安装过 Apifox"""
    paths = [
        expand_path("~/.config/apifox"),
        expand_path("~/.local/share/apifox"),
        expand_path("~/snap/apifox"),
    ]
    installed = []
    for p in paths:
        if Path(p).exists():
            installed.append(p)
    return installed


def check_apifox_installed_windows():
    """检查 Windows 上是否安装过 Apifox"""
    paths = [
        os.path.join(os.environ.get("APPDATA", ""), APIFOX_APP_NAME),
        os.path.join(os.environ.get("LOCALAPPDATA", ""), APIFOX_APP_NAME),
        os.path.join(os.environ.get("APPDATA", ""), "ApiFox"),
        os.path.join(os.environ.get("LOCALAPPDATA", ""), "ApiFox"),
        r"C:\Program Files\ApiFox",
        r"C:\Users\{}\AppData\Roaming\ApiFox".format(os.environ.get("USERNAME", "")),
    ]
    installed = []
    for p in paths:
        if not p:
            continue
        if Path(p).exists():
            installed.append(p)
    return installed


def check_dns_cache():
    """检查 hosts 文件和 DNS 缓存"""
    issues = []
    # macOS / Linux hosts
    if get_os() in ("macos", "linux"):
        hosts = expand_path("~/.hosts") if Path(expand_path("~/.hosts")).exists() else "/etc/hosts"
        if Path(hosts).exists():
            out, _ = run_cmd(f"grep -i '{MALICIOUS_DOMAIN}' '{hosts}' 2>/dev/null || true")
            if out:
                issues.append({"file": hosts, "issue": out})
    # Windows hosts
    elif get_os() == "windows":
        hosts = r"C:\Windows\System32\drivers\etc\hosts"
        if Path(hosts).exists():
            out, _ = run_cmd(f'findstr /I "{MALICIOUS_DOMAIN}" "{hosts}" 2>NUL || true')
            if out:
                issues.append({"file": hosts, "issue": out})
    return issues


def check_git_credential():
    """检查 Git 凭证中是否有可疑 URL"""
    results = []
    # ~/.git-credentials
    git_cred = expand_path("~/.git-credentials")
    if Path(git_cred).exists():
        out, _ = run_cmd(f"grep -i '{MALICIOUS_DOMAIN}' '{git_cred}' 2>/dev/null || true")
        if out:
            results.append({"file": git_cred, "issue": "发现可疑凭证"})
    # git config --global
    out, _ = run_cmd("git config --global --list 2>/dev/null || true")
    if MALICIOUS_DOMAIN.lower() in out.lower():
        results.append({"file": "~/.gitconfig", "issue": "gitconfig中发现可疑域名"})
    return results


def main():
    os_type = get_os()
    print(f"🔍 当前系统: {os_type.upper()}")
    print(f"🎯 恶意域名: {MALICIOUS_DOMAIN}")
    print("=" * 60)

    infected_nws = []
    clean_nws = []
    apifox_dirs = []

    # 1. Network Persistent State 检查
    print("\n📡 [1/4] 检查 Network Persistent State...")
    if os_type == "macos":
        nws = check_nwstate_macos()
    elif os_type == "linux":
        nws = check_nwstate_linux()
    elif os_type == "windows":
        nws = check_nwstate_windows()
    else:
        nws = []
        print("  ⚠️ 未知系统类型，跳过 Network Persistent State 检查")

    for n in nws:
        if n["status"] == "INFECTED":
            infected_nws.append(n)
            print(f"  🔴 感染: {n['file']}")
            print(f"     → {n['detail']}")
        else:
            clean_nws.append(n)

    if not nws:
        print("  ℹ️  未找到 Network Persistent State 文件")

    # 2. Apifox 安装目录检查
    print("\n📁 [2/4] 检查 Apifox 安装目录...")
    if os_type == "macos":
        apifox_dirs = check_apifox_installed_macos()
    elif os_type == "linux":
        apifox_dirs = check_apifox_installed_linux()
    elif os_type == "windows":
        apifox_dirs = check_apifox_installed_windows()

    if apifox_dirs:
        print(f"  ⚠️  发现 {len(apifox_dirs)} 个 Apifox 相关目录:")
        for d in apifox_dirs:
            print(f"     - {d}")
    else:
        print("  ✅ 未发现 Apifox 安装目录")

    # 3. hosts / DNS 检查
    print("\n🌐 [3/4] 检查 hosts / DNS 缓存...")
    dns_issues = check_dns_cache()
    if dns_issues:
        for issue in dns_issues:
            print(f"  🔴 {issue['file']}: {issue['issue']}")
    else:
        print("  ✅ hosts 文件无异常")

    # 4. Git 凭证检查
    print("\n🔑 [4/4] 检查 Git 凭证...")
    git_issues = check_git_credential()
    if git_issues:
        for issue in git_issues:
            print(f"  🔴 {issue['file']}: {issue['issue']}")
    else:
        print("  ✅ Git 凭证无异常")

    # 汇总
    print("\n" + "=" * 60)
    print("📋 检查结果汇总:")
    print(f"  Network Persistent State 感染文件: {len(infected_nws)}")
    print(f"  Network Persistent State 正常文件: {len(clean_nws)}")
    print(f"  Apifox 安装目录数: {len(apifox_dirs)}")
    print(f"  hosts 问题数: {len(dns_issues)}")
    print(f"  Git 凭证问题数: {len(git_issues)}")
    print("=" * 60)

    if infected_nws or dns_issues or git_issues:
        print("\n🚨 结论: 可能已中招！建议立即采取以下措施:")
        print("  1. 立即断网（拔网线/关闭Wi-Fi）")
        print("  2. 彻底卸载 Apifox，结束所有相关进程")
        print("  3. 轮换所有凭证（SSH密钥、Git Token、服务器密码等）")
        return "INFECTED"
    elif apifox_dirs:
        print("\n⚠️  结论: 虽未发现恶意域名记录，但检测到 Apifox 安装目录")
        print("  建议: 卸载 Apifox，或前往官网下载最新版（2.8.21+）重装")
        return "WARNING"
    else:
        print("\n✅ 结论: 未检测到恶意域名记录，也未发现 Apifox 安装痕迹")
        print("  你的系统安全，可以放心。")
        return "CLEAN"


if __name__ == "__main__":
    result = main()
    sys.exit(0 if result == "CLEAN" else 1)
