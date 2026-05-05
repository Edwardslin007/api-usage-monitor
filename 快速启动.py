#!/usr/bin/env python3
"""
快速启动脚本 - 帮助用户快速使用工具
"""

import os
import sys
import subprocess

def check_auth_info():
    """检查认证信息是否存在"""
    auth_file = os.path.expanduser("~/Desktop/ApiUsageMonitor/auth_info.json")
    return os.path.exists(auth_file)

def run_setup():
    """运行设置脚本"""
    print("正在启动认证信息设置向导...")
    subprocess.run([sys.executable, os.path.expanduser("~/Desktop/ApiUsageMonitor/setup_auth.py")])

def run_monitor():
    """运行监控脚本"""
    print("正在启动用量监控...")
    subprocess.run([sys.executable, os.path.expanduser("~/Desktop/ApiUsageMonitor/simple_monitor.py")])

def main():
    """主函数"""
    print("=" * 60)
    print("🎯 API 用量监控工具 - 快速启动")
    print("=" * 60)
    print()
    print("选择操作：")
    print("1. 设置认证信息（首次使用）")
    print("2. 运行用量监控")
    print("3. 退出")
    print()

    choice = input("请输入选择 (1/2/3): ").strip()

    if choice == '1':
        run_setup()
        print("\n设置完成后，请选择选项2运行监控")
    elif choice == '2':
        if not check_auth_info():
            print("\n⚠️  未找到认证信息")
            print("请先选择选项1设置认证信息")
        else:
            run_monitor()
    elif choice == '3':
        print("退出程序")
        sys.exit(0)
    else:
        print("❌ 无效选择")

if __name__ == "__main__":
    main()
