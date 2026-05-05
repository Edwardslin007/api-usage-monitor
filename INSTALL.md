# 🚀 API用量监控工具 - 安装说明

## 📋 前置条件

### 1. Python环境
确保已安装Python 3.6或更高版本：
```bash
python3 --version
```

### 2. 安装依赖
```bash
pip3 install requests
```

---

## 🎯 快速安装（3步完成）

### 第1步：克隆仓库
```bash
git clone https://github.com/your-username/api-usage-monitor.git
cd api-usage-monitor
```

### 第2步：设置认证信息
```bash
python3 快速启动.py
# 选择选项1，按照提示获取认证信息
```

### 第3步：运行监控
```bash
python3 simple_monitor.py
```

---

## 📝 详细安装说明

### 步骤1：获取认证信息

#### 方法A：使用设置脚本（推荐）
```bash
python3 setup_auth.py
```
按照提示操作，获取Authorization Token。

#### 方法B：手动设置
1. 打开Chrome浏览器
2. 访问 https://v2.aicodee.com/console/topup
3. 按F12打开开发者工具
4. 切换到Network标签
5. 刷新页面
6. 找到API请求（如 `/api/user/info`）
7. 查看请求头中的Authorization
8. 复制值（格式：`Bearer xxxxxxxx`）

### 步骤2：创建认证信息文件
创建 `auth_info.json` 文件，内容如下：
```json
{
    "type": "token",
    "value": "Bearer your_token_here"
}
```

### 步骤3：验证安装
```bash
python3 simple_monitor.py
```
如果显示用量信息，说明安装成功。

---

## 🎯 使用方法

### 日常使用
```bash
cd api-usage-monitor
python3 simple_monitor.py
```

### 创建快捷方式（Mac/Linux）
```bash
echo 'python3 /path/to/api-usage-monitor/simple_monitor.py' > ~/check_usage.sh
chmod +x ~/check_usage.sh
```

### 创建快捷方式（Windows）
创建 `check_usage.bat` 文件，内容：
```batch
python C:\path\to\api-usage-monitor\simple_monitor.py
```

---

## 🔧 常见问题

### 问题1：Python未安装
**解决方案**：
- Mac：`brew install python3`
- Windows：从官网下载Python
- Linux：`sudo apt-get install python3`

### 问题2：requests库未安装
**解决方案**：
```bash
pip3 install requests
```

### 问题3：认证信息错误
**解决方案**：
1. 重新获取Token
2. 检查Token格式（应以`Bearer`开头）
3. 确认Token未过期

### 问题4：无法连接到API
**解决方案**：
1. 检查网络连接
2. 确认API地址正确
3. 检查防火墙设置

---

## 📊 验证安装成功

运行以下命令验证：
```bash
python3 simple_monitor.py
```

**预期输出**：
```
============================================================
API 用量监控工具 - 简化版本
============================================================

使用认证方式: token
尝试 /api/user/info...
✅ 成功获取数据

============================================================
📊 用量信息
============================================================
剩余$28.30（94%），距离额度重置剩余x小时x分。套餐剩余17天，至 5/22/2026, 10:30:26 AM
============================================================
```

---

## 💡 使用提示

1. **定期更新Token**：Token通常有有效期，需要定期更新
2. **保护认证信息**：不要将 `auth_info.json` 提交到GitHub
3. **查看历史数据**：用量数据保存在 `usage_cache.json` 文件中
4. **集成到其他系统**：可以将 `simple_monitor.py` 导入到其他项目

---

## 📞 需要帮助？

1. 查看 `新版本使用说明.md` 获取详细说明
2. 查看 `README.md` 了解项目概况
3. 查看 `常见问题.md` 解决问题

---

**安装完成时间**: [当前时间]
**安装人员**: [你的名字]
**版本**: v1.0
