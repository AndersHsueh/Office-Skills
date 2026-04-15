#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
update_gh_host.py - 更新本地hosts文件以优化GitHub访问的脚本
"""
import os
import re
import sys
import tempfile
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

def get_system_hosts_path():
    """
    获取不同操作系统的hosts文件路径
    """
    if sys.platform.startswith('win'):
        return r"C:\Windows\System32\drivers\etc\hosts"
    elif sys.platform.startswith('darwin') or 'linux' in sys.platform:
        return "/etc/hosts"
    else:
        raise OSError("不支持的操作系统")


def backup_hosts_file(hosts_path):
    """
    备份hosts文件
    """
    backup_path = f"{hosts_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    shutil.copy2(hosts_path, backup_path)
    print(f"已备份原hosts文件至: {backup_path}")
    return backup_path


def get_latest_hosts_content():
    """
    从GitHub520项目获取最新的hosts内容，支持备用源
    """
    import urllib.request
    import urllib.error
    
    # 主要和备用URL列表
    urls = [
        "https://raw.hellogithub.com/hosts",  # 主要源
        "https://gitee.com/andershsueh/git-hub520ax/raw/main/hosts"  # 备用源
    ]
    
    for url in urls:
        try:
            print(f"正在从 {url} 获取最新hosts内容...")
            with urllib.request.urlopen(url, timeout=30) as response:
                content = response.read().decode('utf-8')
            print("获取成功！")
            return content
        except urllib.error.URLError as e:
            print(f"从 {url} 获取hosts内容失败: {e}")
            continue  # 尝试下一个URL
    
    print("所有hosts内容源都不可用")
    return None


def update_hosts_file():
    """
    更新hosts文件中的GitHub相关条目
    """
    hosts_path = get_system_hosts_path()
    
    # 检查hosts文件是否存在
    if not os.path.exists(hosts_path):
        print(f"错误: hosts文件不存在于: {hosts_path}")
        return False
    
    # 备份原hosts文件
    try:
        backup_path = backup_hosts_file(hosts_path)
    except Exception as e:
        print(f"备份hosts文件失败: {e}")
        return False
    
    # 获取最新的hosts内容
    latest_content = get_latest_hosts_content()
    if not latest_content:
        print("获取最新hosts内容失败，恢复备份文件")
        try:
            shutil.copy2(backup_path, hosts_path)
        except Exception:
            pass
        return False
    
    # 读取当前hosts文件内容
    try:
        with open(hosts_path, 'r', encoding='utf-8') as f:
            current_content = f.read()
    except Exception as e:
        print(f"读取hosts文件失败: {e}")
        return False
    
    # 查找并替换现有的GitHub520条目
    start_marker = "# GitHub520 Host Start"
    end_marker = "# GitHub520 Host End"
    
    # 正则表达式匹配整个GitHub520块
    pattern = re.compile(f"{re.escape(start_marker)}.*?{re.escape(end_marker)}", re.DOTALL)
    
    # 检查是否已有GitHub520条目
    if pattern.search(current_content):
        # 替换现有条目
        updated_content = pattern.sub(latest_content.strip(), current_content)
    else:
        # 添加新条目到文件末尾
        updated_content = current_content.rstrip() + "\n\n" + latest_content.strip()
    
    # 写入更新后的内容
    try:
        # 使用临时文件避免写入中断导致hosts损坏
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8', dir=os.path.dirname(hosts_path)) as tmp_file:
            tmp_file.write(updated_content)
            tmp_path = tmp_file.name
        
        # 移动临时文件覆盖原hosts文件
        # 在Windows上需要特殊处理
        if sys.platform.startswith('win'):
            os.chmod(tmp_path, 0o644)
            shutil.move(tmp_path, hosts_path)
        else:
            shutil.move(tmp_path, hosts_path)
        
        print(f"hosts文件已成功更新！")
        print(f"原文件已备份至: {backup_path}")
        return True
    except PermissionError:
        print("错误: 没有权限修改hosts文件，请以管理员身份运行此脚本")
        # 恢复备份
        try:
            shutil.copy2(backup_path, hosts_path)
        except Exception:
            pass
        return False
    except Exception as e:
        print(f"更新hosts文件失败: {e}")
        # 恢复备份
        try:
            shutil.copy2(backup_path, hosts_path)
        except Exception:
            pass
        return False


def flush_dns_cache():
    """
    刷新DNS缓存
    """
    print("\n正在刷新DNS缓存...")
    
    try:
        if sys.platform.startswith('win'):
            result = subprocess.run(['ipconfig', '/flushdns'], capture_output=True, text=True)
            print(result.stdout)
        elif sys.platform.startswith('darwin'):
            result = subprocess.run(['sudo', 'killall', '-HUP', 'mDNSResponder'], capture_output=True, text=True)
            print(result.stdout)
            if result.stderr:
                print(f"警告: {result.stderr}")
        elif 'linux' in sys.platform:
            # 尝试多种常见的DNS缓存服务
            services = ['nscd', 'systemd-resolved']
            for service in services:
                try:
                    result = subprocess.run(['sudo', 'service', service, 'restart'], capture_output=True, text=True)
                    if result.returncode == 0:
                        print(f"已重启 {service} 服务")
                        break
                    else:
                        print(f"重启 {service} 服务失败: {result.stderr}")
                except FileNotFoundError:
                    continue
        else:
            print("请手动刷新DNS缓存")
    except Exception as e:
        print(f"刷新DNS缓存时出错: {e}")


def main():
    """
    主函数
    """
    print("GitHub Hosts 更新工具")
    print("=" * 40)
    
    success = update_hosts_file()
    
    if success:
        print("\n更新完成！为了使更改立即生效，建议刷新DNS缓存。")
        flush_dns_cache()
        print("\n现在您可以访问GitHub来测试连接速度是否改善。")
    else:
        print("\n更新失败，请检查错误信息。")


if __name__ == "__main__":
    main()