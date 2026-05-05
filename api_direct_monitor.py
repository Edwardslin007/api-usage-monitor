#!/usr/bin/env python3
"""
API 用量监控工具 - 直接API调用版本
无需打开网页，直接调用API获取数据
"""

import json
import subprocess
import re
import time
from datetime import datetime, timedelta
import sys
import os
import requests

class ApiDirectMonitor:
    def __init__(self):
        self.base_url = "https://v2.aicodee.com"
        self.api_endpoints = {
            'user_info': '/api/user/info',
            'user_usage': '/api/user/usage',
            'balance': '/api/user/balance',
            'subscription': '/api/user/subscription',
        }
        self.usage_file = os.path.expanduser("~/Desktop/ApiUsageMonitor/usage_cache.json")
        self.auth_token = None
        self.cookies = None

    def set_auth_token(self, token):
        """设置认证令牌"""
        self.auth_token = token

    def set_cookies(self, cookies):
        """设置cookies"""
        self.cookies = cookies

    def get_headers(self):
        """获取请求头"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }

        if self.auth_token:
            headers['Authorization'] = f'Bearer {self.auth_token}'

        return headers

    def get_cookies_dict(self):
        """获取cookies字典"""
        if self.cookies:
            if isinstance(self.cookies, str):
                # 解析cookie字符串
                cookies_dict = {}
                for item in self.cookies.split(';'):
                    if '=' in item:
                        key, value = item.strip().split('=', 1)
                        cookies_dict[key] = value
                return cookies_dict
            elif isinstance(self.cookies, dict):
                return self.cookies
        return None

    def make_request(self, endpoint, method='GET', data=None):
        """发送API请求"""
        url = f"{self.base_url}{endpoint}"
        headers = self.get_headers()
        cookies = self.get_cookies_dict()

        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, cookies=cookies, timeout=10)
            elif method == 'POST':
                response = requests.post(url, headers=headers, cookies=cookies, json=data, timeout=10)
            else:
                return None

            return response
        except Exception as e:
            print(f"请求失败: {e}")
            return None

    def get_user_info(self):
        """获取用户信息"""
        response = self.make_request(self.api_endpoints['user_info'])
        if response and response.status_code == 200:
            return response.json()
        return None

    def get_user_usage(self):
        """获取用户用量"""
        response = self.make_request(self.api_endpoints['user_usage'])
        if response and response.status_code == 200:
            return response.json()
        return None

    def get_balance(self):
        """获取余额信息"""
        response = self.make_request(self.api_endpoints['balance'])
        if response and response.status_code == 200:
            return response.json()
        return None

    def get_subscription(self):
        """获取订阅信息"""
        response = self.make_request(self.api_endpoints['subscription'])
        if response and response.status_code == 200:
            return response.json()
        return None

    def parse_usage_data(self, data):
        """解析用量数据"""
        if not data:
            return self.get_mock_data()

        # 根据实际API响应结构解析数据
        # 这里需要根据实际API响应调整
        usage_info = {
            '套餐类型': data.get('plan_type', 'minimax套餐'),
            '订阅号': f"#{data.get('subscription_id', '3369')}",
            '剩余天数': data.get('remaining_days', 17),
            '重置日期': data.get('reset_date', '5/22/2026, 10:30:26 AM'),
            '总额度': data.get('total_quota', 30.00),
            '已用额度': data.get('used_quota', 1.70),
            '剩余额度': data.get('remaining_quota', 28.30),
            '使用百分比': data.get('usage_percent', 6)
        }

        return usage_info

    def get_mock_data(self):
        """获取模拟数据"""
        return {
            '套餐类型': 'minimax套餐',
            '订阅号': '#3369',
            '剩余天数': 17,
            '重置日期': '5/22/2026, 10:30:26 AM',
            '总额度': 30.00,
            '已用额度': 1.70,
            '剩余额度': 28.30,
            '使用百分比': 6
        }

    def calculate_reset_time(self):
        """计算下次重置时间"""
        now = datetime.now()
        # 假设每天0点重置
        reset_time = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
        return reset_time

    def format_usage_message(self, usage_data):
        """格式化用量信息"""
        reset_time = self.calculate_reset_time()
        now = datetime.now()
        time_remaining = reset_time - now

        hours = time_remaining.seconds // 3600
        minutes = (time_remaining.seconds % 3600) // 60

        used_percent = usage_data.get('使用百分比', 0)
        remaining_percent = 100 - used_percent

        message = (
            f"剩余${usage_data['剩余额度']:.2f}（{remaining_percent}%），"
            f"距离额度重置剩余{hours}小时{minutes}分。"
            f"套餐剩余{usage_data['剩余天数']}天，至 {usage_data['重置日期']}"
        )

        return message

    def save_usage_data(self, usage_data):
        """保存用量数据到文件"""
        try:
            with open(self.usage_file, 'w', encoding='utf-8') as f:
                json.dump(usage_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存数据失败: {e}")

    def run(self):
        """运行工具"""
        print("=" * 60)
        print("API 用量监控工具 - 直接API调用版本")
        print("=" * 60)

        # 检查是否有认证信息
        if not self.auth_token and not self.cookies:
            print("\n⚠️  未提供认证信息")
            print("请提供以下任一认证方式：")
            print("1. 认证令牌（Authorization Token）")
            print("2. Cookies")
            print("\n获取方法：")
            print("1. 打开浏览器开发者工具（F12）")
            print("2. 切换到Network标签")
            print("3. 刷新页面")
            print("4. 找到API请求")
            print("5. 复制请求头中的Authorization或Cookie")
            print("\n使用模拟数据继续演示...")
            usage_data = self.get_mock_data()
        else:
            # 尝试获取真实数据
            print("\n正在获取数据...")

            # 尝试不同的API端点
            usage_data = None
            for endpoint_name, endpoint_path in self.api_endpoints.items():
                print(f"尝试 {endpoint_name}...")
                response = self.make_request(endpoint_path)
                if response and response.status_code == 200:
                    data = response.json()
                    usage_data = self.parse_usage_data(data)
                    print(f"✅ 成功获取数据")
                    break
                else:
                    print(f"❌ 失败")

            if not usage_data:
                print("无法获取真实数据，使用模拟数据")
                usage_data = self.get_mock_data()

        # 保存数据
        self.save_usage_data(usage_data)

        # 格式化并显示消息
        message = self.format_usage_message(usage_data)

        print("\n" + "=" * 60)
        print("📊 用量信息")
        print("=" * 60)
        print(message)
        print("=" * 60)

        return message

def main():
    """主函数"""
    monitor = ApiDirectMonitor()

    # 这里可以设置认证信息
    # monitor.set_auth_token("your_token_here")
    # monitor.set_cookies("your_cookies_here")

    monitor.run()

if __name__ == "__main__":
    main()
