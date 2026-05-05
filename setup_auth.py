#!/usr/bin/env python3
"""
认证信息设置脚本
帮助用户设置API认证信息
"""

import json
import os
import sys

def save_auth_info(auth_type, auth_value):
    """保存认证信息到文件"""
    auth_file = os.path.expanduser("~/Desktop/ApiUsageMonitor/auth_info.json")
    auth_data = {
        'type': auth_type,
        'value': auth_value
    }

    with open(auth_file, 'w', encoding='utf-8') as f:
        json.dump(auth_data, f, ensure_ascii=False, indent=2)

    print(f"\n✅ 认证信息已保存到: {auth_file}")
    return True

def main():
    """主函数"""
    print("=" * 60)
    print("🔑 API认证信息设置工具")
    print("=" * 60)
    print()
    print("请选择认证方式：")
    print("1. Authorization Token（推荐）")
    print("2. Cookies")
    print("3. 退出")
    print()

    choice = input("请输入选择 (1/2/3): ").strip()

    if choice == '1':
        print("\n📋 获取Authorization Token的步骤：")
        print("1. 打开Chrome浏览器")
        print("2. 访问 https://v2.aicodee.com/console/topup")
        print("3. 按F12打开开发者工具")
        print("4. 切换到Network标签")
        print("5. 刷新页面")
        print("6. 找到API请求（如 /api/user/info）")
        print("7. 查看请求头中的Authorization")
        print("8. 复制值（格式：Bearer xxxxxxxx）")
        print()

        token = input("请粘贴Authorization Token: ").strip()
        if token:
            save_auth_info('token', token)
        else:
            print("❌ Token不能为空")

    elif choice == '2':
        print("\n📋 获取Cookies的步骤：")
        print("1. 打开Chrome浏览器")
        print("2. 访问 https://v2.aicodee.com/console/topup")
        print("3. 按F12打开开发者工具")
        print("4. 切换到Application标签")
        print("5. 展开Cookies")
        print("6. 点击 https://v2.aicodee.com")
        print("7. 复制所有Cookie值")
        print()

        cookies = input("请粘贴Cookies: ").strip()
        if cookies:
            save_auth_info('cookies', cookies)
        else:
            print("❌ Cookies不能为空")

    elif choice == '3':
        print("退出设置")
        sys.exit(0)

    else:
        print("❌ 无效选择")

if __name__ == "__main__":
    main()
