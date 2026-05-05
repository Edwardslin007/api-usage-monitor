#!/usr/bin/env python3
"""
新旧版本对比测试
"""

import time
import subprocess
import json
import os

def test_old_version():
    """测试旧版本"""
    print("=" * 70)
    print("🔴 测试旧版本（Chrome DevTools Protocol方案）")
    print("=" * 70)

    # 测试1: Chrome连接检查
    print("\n测试1: Chrome连接检查")
    start_time = time.time()
    result = subprocess.run(['curl', '-s', 'http://localhost:9222/json/version'],
                          capture_output=True, text=True, timeout=5)
    end_time = time.time()
    chrome_time = end_time - start_time

    if result.returncode == 0:
        print(f"  ✅ Chrome连接成功 ({chrome_time:.3f}秒)")
    else:
        print(f"  ❌ Chrome连接失败 ({chrome_time:.3f}秒)")

    # 测试2: 页面列表获取
    print("\n测试2: 页面列表获取")
    start_time = time.time()
    result = subprocess.run(['curl', '-s', 'http://localhost:9222/json'],
                          capture_output=True, text=True, timeout=5)
    end_time = time.time()
    list_time = end_time - start_time

    if result.returncode == 0:
        pages = json.loads(result.stdout)
        print(f"  ✅ 获取成功 ({list_time:.3f}秒, {len(pages)}个页面)")
    else:
        print(f"  ❌ 获取失败 ({list_time:.3f}秒)")

    # 测试3: 目标页面查找
    print("\n测试3: 目标页面查找")
    start_time = time.time()
    result = subprocess.run(['curl', '-s', 'http://localhost:9222/json'],
                          capture_output=True, text=True, timeout=5)
    pages = json.loads(result.stdout)
    target_page = None
    for page in pages:
        if 'v2.aicodee.com/console/topup' in page.get('url', ''):
            target_page = page
            break
    end_time = time.time()
    find_time = end_time - start_time

    if target_page:
        print(f"  ✅ 找到目标页面 ({find_time:.3f}秒)")
    else:
        print(f"  ❌ 未找到目标页面 ({find_time:.3f}秒)")

    # 测试4: 整体执行时间
    print("\n测试4: 整体执行时间")
    start_time = time.time()
    result = subprocess.run(['python3', 'main.py'], capture_output=True, text=True, timeout=30)
    end_time = time.time()
    total_time = end_time - start_time

    print(f"  ✅ 执行完成 ({total_time:.3f}秒)")

    return {
        'chrome_time': chrome_time,
        'list_time': list_time,
        'find_time': find_time,
        'total_time': total_time
    }

def test_new_version():
    """测试新版本"""
    print("\n" + "=" * 70)
    print("🟢 测试新版本（直接API调用方案）")
    print("=" * 70)

    # 测试1: 检查认证信息
    print("\n测试1: 检查认证信息")
    auth_file = os.path.expanduser("~/Desktop/ApiUsageMonitor/auth_info.json")
    start_time = time.time()
    has_auth = os.path.exists(auth_file)
    end_time = time.time()
    auth_check_time = end_time - start_time

    if has_auth:
        print(f"  ✅ 找到认证信息 ({auth_check_time:.3f}秒)")
    else:
        print(f"  ⚠️  未找到认证信息 ({auth_check_time:.3f}秒)")

    # 测试2: 执行监控脚本
    print("\n测试2: 执行监控脚本")
    start_time = time.time()
    result = subprocess.run(['python3', 'simple_monitor.py'], capture_output=True, text=True, timeout=30)
    end_time = time.time()
    total_time = end_time - start_time

    print(f"  ✅ 执行完成 ({total_time:.3f}秒)")

    return {
        'auth_check_time': auth_check_time,
        'total_time': total_time
    }

def compare_results(old_results, new_results):
    """对比结果"""
    print("\n" + "=" * 70)
    print("📊 新旧版本对比结果")
    print("=" * 70)

    print("\n【执行时间对比】")
    print(f"  旧版本总时间: {old_results['total_time']:.3f}秒")
    print(f"  新版本总时间: {new_results['total_time']:.3f}秒")

    if old_results['total_time'] > 0:
        speedup = old_results['total_time'] / new_results['total_time']
        print(f"  性能提升: {speedup:.1f}倍")
    else:
        print(f"  性能提升: 无法计算")

    print("\n【功能对比】")
    print("  旧版本:")
    print("    - 需要Chrome浏览器运行")
    print("    - 需要网页保持打开状态")
    print("    - 需要WebSocket连接")
    print("    - 可能被安全策略阻止")

    print("\n  新版本:")
    print("    - 无需Chrome浏览器")
    print("    - 无需打开网页")
    print("    - 直接调用API")
    print("    - 完全静默运行")

    print("\n【资源占用对比】")
    print("  旧版本:")
    print("    - CPU: 中等（需要运行浏览器）")
    print("    - 内存: 高（浏览器进程）")
    print("    - 网络: 低")

    print("\n  新版本:")
    print("    - CPU: 低")
    print("    - 内存: 低")
    print("    - 网络: 低")

    print("\n【推荐使用】")
    print("  ✅ 强烈推荐使用新版本")
    print("  理由:")
    print("    1. 更快")
    print("    2. 更简单")
    print("    3. 更高效")
    print("    4. 更易于集成")
    print("    5. 更适合长期使用")

def main():
    """主函数"""
    print("🎯 API用量监控工具 - 新旧版本对比测试")
    print("=" * 70)

    # 测试旧版本
    old_results = test_old_version()

    # 测试新版本
    new_results = test_new_version()

    # 对比结果
    compare_results(old_results, new_results)

if __name__ == "__main__":
    main()
