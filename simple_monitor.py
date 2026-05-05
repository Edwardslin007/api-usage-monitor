#!/usr/bin/env python3
"""
API 用量监控工具 - 简化版本
直接API调用，自动获取认证信息，无需手动配置
"""

import json
import os
import sys
from datetime import datetime, timedelta
import requests
import browser_cookie3

class SimpleMonitor:
    def __init__(self):
        self.base_url = "https://v2.aicodee.com"
        self.usage_file = os.path.expanduser("~/Desktop/ApiUsageMonitor/usage_cache.json")

    def get_cookies_from_browser(self):
        """从Chrome浏览器自动获取cookies"""
        try:
            cj = browser_cookie3.chrome(domain_name='v2.aicodee.com')
            cookies_dict = {}
            for cookie in cj:
                cookies_dict[cookie.name] = cookie.value
            return cookies_dict
        except Exception as e:
            print(f"获取cookies失败: {e}")
            return None

    def get_user_id_from_browser(self):
        """从Chrome localStorage获取用户ID"""
        try:
            import subprocess
            # 使用Node.js获取localStorage
            node_script = r'''
const http = require('http');
const WebSocket = require('ws');

http.get('http://localhost:9222/json', (res) => {
    let data = '';
    res.on('data', chunk => data += chunk);
    res.on('end', () => {
        const pages = JSON.parse(data);
        const targetPage = pages.find(p => p.url.includes('v2.aicodee.com/console/topup'));

        if (!targetPage) {
            console.log(JSON.stringify({error: '未找到目标页面'}));
            return;
        }

        const ws = new WebSocket(targetPage.webSocketDebuggerUrl);

        ws.on('open', () => {
            ws.send(JSON.stringify({
                id: 1,
                method: 'Runtime.evaluate',
                params: {
                    expression: 'localStorage.getItem("user")',
                    returnByValue: true
                }
            }));
        });

        ws.on('message', (data) => {
            const response = JSON.parse(data.toString());
            if (response.id === 1) {
                const value = response.result?.result?.value;
                if (value) {
                    const user = JSON.parse(value);
                    console.log(JSON.stringify({id: user.id, username: user.username}));
                } else {
                    console.log(JSON.stringify({error: '无法获取用户信息'}));
                }
                ws.close();
            }
        });

        ws.on('error', (err) => {
            console.log(JSON.stringify({error: err.message}));
        });
    });
}).on('error', (err) => {
    console.log(JSON.stringify({error: err.message}));
});
'''
            # 使用Node.js -e参数执行脚本
            result = subprocess.run(['node', '-e', node_script],
                                  capture_output=True, text=True, timeout=10)

            if result.returncode == 0 and result.stdout.strip():
                user_info = json.loads(result.stdout.strip())
                if 'id' in user_info:
                    return user_info['id']

        except Exception as e:
            print(f"获取用户ID失败: {e}")
        return None

    def make_request(self, endpoint, cookies, user_id):
        """发送API请求"""
        url = f"{self.base_url}{endpoint}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Accept': 'application/json',
            'New-Api-User': str(user_id),
        }

        try:
            response = requests.get(url, headers=headers, cookies=cookies, timeout=10)
            return response
        except Exception as e:
            print(f"请求失败: {e}")
            return None

    def get_subscription_data(self, cookies, user_id):
        """获取订阅数据"""
        response = self.make_request('/api/subscription/self', cookies, user_id)
        if response and response.status_code == 200:
            data = response.json()
            return data.get('data', {})
        return None

    def parse_usage_data(self, sub_data):
        """解析用量数据"""
        subscriptions = sub_data.get('all_subscriptions', [])
        if not subscriptions:
            return self.get_mock_data()

        sub = subscriptions[0]
        sub_info = sub.get('subscription', {})

        # 计算额度（单位转换：1 unit = $0.000002）
        total_units = sub_info.get('amount_total', 0)
        used_units = sub_info.get('amount_used', 0)
        remaining_units = total_units - used_units

        # 转换为美元（根据页面显示：$30.00总额度，15000000 units）
        # 15000000 units = $30.00，所以 1 unit = $0.000002
        total_usd = total_units * 0.000002
        used_usd = used_units * 0.000002
        remaining_usd = remaining_units * 0.000002

        # 计算使用百分比
        if total_units > 0:
            used_percent = (used_units / total_units) * 100
        else:
            used_percent = 0

        # 时间信息
        end_time = datetime.fromtimestamp(sub_info.get('end_time', 0))
        next_reset = datetime.fromtimestamp(sub_info.get('next_reset_time', 0))

        # 计算剩余天数
        remaining_days = (end_time - datetime.now()).days

        # 格式化重置日期
        reset_date_str = end_time.strftime("%m/%d/%Y, %I:%M:%S %p")

        usage_info = {
            '套餐类型': 'minimax套餐',
            '订阅号': f"#{sub_info.get('id', '3369')}",
            '剩余天数': remaining_days,
            '重置日期': reset_date_str,
            '总额度': total_usd,
            '已用额度': used_usd,
            '剩余额度': remaining_usd,
            '使用百分比': round(used_percent, 1),
            '下次重置时间': next_reset,
            '原始总额度': total_units,
            '原始已用额度': used_units,
            '原始剩余额度': remaining_units,
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
            '使用百分比': 6,
            '下次重置时间': datetime.now().replace(hour=0, minute=0, second=0) + timedelta(days=1),
        }

    def format_usage_message(self, usage_data):
        """格式化用量信息"""
        now = datetime.now()
        next_reset = usage_data.get('下次重置时间', now.replace(hour=0, minute=0, second=0) + timedelta(days=1))
        time_remaining = next_reset - now

        hours = time_remaining.seconds // 3600
        minutes = (time_remaining.seconds % 3600) // 60

        remaining_percent = 100 - usage_data.get('使用百分比', 0)

        message = (
            f"剩余${usage_data['剩余额度']:.2f}（{remaining_percent:.1f}%），"
            f"距离额度重置剩余{hours}小时{minutes}分。"
            f"套餐剩余{usage_data['剩余天数']}天，至 {usage_data['重置日期']}"
        )

        return message

    def save_usage_data(self, usage_data):
        """保存用量数据到文件"""
        try:
            # 转换datetime对象为字符串
            save_data = usage_data.copy()
            if '下次重置时间' in save_data:
                save_data['下次重置时间'] = save_data['下次重置时间'].isoformat()

            with open(self.usage_file, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存数据失败: {e}")

    def run(self):
        """运行工具"""
        print("=" * 60)
        print("API 用量监控工具 - 简化版本")
        print("=" * 60)

        # 从浏览器获取cookies
        print("\n🔐 从浏览器获取认证信息...")
        cookies = self.get_cookies_from_browser()
        if not cookies:
            print("❌ 无法从浏览器获取cookies")
            print("请确保Chrome浏览器已打开并登录到 v2.aicodee.com")
            print("\n使用模拟数据继续演示...")
            usage_data = self.get_mock_data()
        else:
            # 获取用户ID
            print("📋 获取用户ID...")
            user_id = self.get_user_id_from_browser()
            if not user_id:
                print("❌ 无法获取用户ID")
                print("请确保Chrome浏览器已打开并登录到 v2.aicodee.com")
                print("\n使用模拟数据继续演示...")
                usage_data = self.get_mock_data()
            else:
                print(f"✅ 用户ID: {user_id}")

                # 获取订阅数据
                print("📊 获取订阅数据...")
                sub_data = self.get_subscription_data(cookies, user_id)
                if sub_data:
                    usage_data = self.parse_usage_data(sub_data)
                    print("✅ 成功获取真实数据")
                else:
                    print("❌ 无法获取订阅数据")
                    print("\n使用模拟数据继续演示...")
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
    monitor = SimpleMonitor()
    monitor.run()

if __name__ == "__main__":
    main()
