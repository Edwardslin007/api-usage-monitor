#!/usr/bin/env python3
"""
一键安装脚本 - 帮助用户快速安装和配置工具
"""

import os
import sys
import subprocess
import json
import platform

class Installer:
    def __init__(self):
        self.system = platform.system()
        self.project_dir = os.path.dirname(os.path.abspath(__file__))
        self.auth_file = os.path.join(self.project_dir, "auth_info.json")

    def print_header(self):
        """打印头部信息"""
        print("=" * 70)
        print("🎯 API用量监控工具 - 一键安装程序")
        print("=" * 70)
        print()
        print("本程序将帮助你快速安装和配置API用量监控工具")
        print()

    def check_python_version(self):
        """检查Python版本"""
        print("📋 步骤1: 检查Python环境")
        print("-" * 50)

        version = sys.version_info
        if version.major >= 3 and version.minor >= 6:
            print(f"  ✅ Python {version.major}.{version.minor}.{version.micro} 已安装")
            return True
        else:
            print(f"  ❌ Python版本过低: {version.major}.{version.minor}.{version.micro}")
            print(f"  需要Python 3.6或更高版本")
            return False

    def install_dependencies(self):
        """安装依赖"""
        print("\n📋 步骤2: 安装依赖包")
        print("-" * 50)

        try:
            # 检查requests是否已安装
            import requests
            print("  ✅ requests库已安装")
            return True
        except ImportError:
            print("  ⚠️  requests库未安装，正在安装...")
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", "requests"],
                             check=True, capture_output=True)
                print("  ✅ requests库安装成功")
                return True
            except subprocess.CalledProcessError as e:
                print(f"  ❌ 安装失败: {e}")
                return False

    def check_auth_info(self):
        """检查认证信息"""
        print("\n📋 步骤3: 检查认证信息")
        print("-" * 50)

        if os.path.exists(self.auth_file):
            print("  ✅ 认证信息已配置")
            return True
        else:
            print("  ⚠️  认证信息未配置")
            return False

    def setup_auth_info(self):
        """设置认证信息"""
        print("\n📋 步骤4: 设置认证信息")
        print("-" * 50)

        print("\n请选择认证方式：")
        print("1. Authorization Token（推荐）")
        print("2. Cookies")
        print("3. 稍后设置")

        choice = input("\n请输入选择 (1/2/3): ").strip()

        if choice == '1':
            return self.setup_token_auth()
        elif choice == '2':
            return self.setup_cookie_auth()
        elif choice == '3':
            print("\n⚠️  跳过认证信息设置")
            print("你可以稍后运行 python3 setup_auth.py 进行设置")
            return False
        else:
            print("\n❌ 无效选择")
            return False

    def setup_token_auth(self):
        """设置Token认证"""
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
            auth_data = {
                'type': 'token',
                'value': token
            }
            with open(self.auth_file, 'w', encoding='utf-8') as f:
                json.dump(auth_data, f, ensure_ascii=False, indent=2)
            print("  ✅ 认证信息保存成功")
            return True
        else:
            print("  ❌ Token不能为空")
            return False

    def setup_cookie_auth(self):
        """设置Cookie认证"""
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
            auth_data = {
                'type': 'cookies',
                'value': cookies
            }
            with open(self.auth_file, 'w', encoding='utf-8') as f:
                json.dump(auth_data, f, ensure_ascii=False, indent=2)
            print("  ✅ 认证信息保存成功")
            return True
        else:
            print("  ❌ Cookies不能为空")
            return False

    def test_installation(self):
        """测试安装"""
        print("\n📋 步骤5: 测试安装")
        print("-" * 50)

        try:
            result = subprocess.run([sys.executable, "simple_monitor.py"],
                                  capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                print("  ✅ 安装测试成功")
                print("\n  测试输出:")
                for line in result.stdout.split('\n'):
                    if line.strip():
                        print(f"    {line}")
                return True
            else:
                print("  ❌ 安装测试失败")
                print(f"  错误信息: {result.stderr}")
                return False
        except Exception as e:
            print(f"  ❌ 测试出错: {e}")
            return False

    def create_shortcut(self):
        """创建快捷方式"""
        print("\n📋 步骤6: 创建快捷方式")
        print("-" * 50)

        if self.system == "Darwin" or self.system == "Linux":
            shortcut_path = os.path.expanduser("~/check_usage.sh")
            shortcut_content = f'#!/bin/bash\npython3 "{self.project_dir}/simple_monitor.py"\n'
        elif self.system == "Windows":
            shortcut_path = os.path.expanduser("~/check_usage.bat")
            shortcut_content = f'python "{self.project_dir}\\simple_monitor.py"\n'
        else:
            print("  ⚠️  不支持的操作系统，跳过创建快捷方式")
            return False

        create = input(f"\n是否创建快捷方式到 {shortcut_path}? (y/n): ").strip().lower()
        if create == 'y':
            try:
                with open(shortcut_path, 'w', encoding='utf-8') as f:
                    f.write(shortcut_content)

                if self.system != "Windows":
                    os.chmod(shortcut_path, 0o755)

                print(f"  ✅ 快捷方式创建成功: {shortcut_path}")
                return True
            except Exception as e:
                print(f"  ❌ 创建失败: {e}")
                return False
        else:
            print("  ⏭️  跳过创建快捷方式")
            return False

    def print_success(self):
        """打印成功信息"""
        print("\n" + "=" * 70)
        print("🎉 安装完成！")
        print("=" * 70)
        print()
        print("📌 使用方法：")
        print("  1. 运行监控: python3 simple_monitor.py")
        if self.system == "Darwin" or self.system == "Linux":
            print("  2. 使用快捷方式: ~/check_usage.sh")
        elif self.system == "Windows":
            print("  2. 使用快捷方式: ~/check_usage.bat")
        print()
        print("📌 其他命令：")
        print("  • 快速启动: python3 快速启动.py")
        print("  • 重新设置认证: python3 setup_auth.py")
        print("  • 查看使用说明: 查看 README.md")
        print()
        print("📌 提示：")
        print("  • Token过期时需要重新设置认证信息")
        print("  • 用量数据会自动保存到 usage_cache.json")
        print()

    def run(self):
        """运行安装程序"""
        self.print_header()

        # 步骤1: 检查Python版本
        if not self.check_python_version():
            print("\n❌ 安装失败：Python版本不符合要求")
            return False

        # 步骤2: 安装依赖
        if not self.install_dependencies():
            print("\n❌ 安装失败：依赖安装失败")
            return False

        # 步骤3: 检查认证信息
        has_auth = self.check_auth_info()

        # 步骤4: 设置认证信息（如果需要）
        if not has_auth:
            if not self.setup_auth_info():
                print("\n⚠️  警告：认证信息未配置，工具可能无法正常工作")

        # 步骤5: 测试安装
        if not self.test_installation():
            print("\n❌ 安装测试失败")
            return False

        # 步骤6: 创建快捷方式
        self.create_shortcut()

        # 打印成功信息
        self.print_success()

        return True

def main():
    """主函数"""
    installer = Installer()
    installer.run()

if __name__ == "__main__":
    main()
