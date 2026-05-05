# 🚀 快速开始指南

## 📋 3步完成安装和使用

### 第1步：下载代码
```bash
git clone https://github.com/your-username/api-usage-monitor.git
cd api-usage-monitor
```

### 第2步：设置认证信息
```bash
python3 setup_auth.py
```
按照提示获取Authorization Token。

### 第3步：运行监控
```bash
python3 simple_monitor.py
```

**完成！** 🎉

---

## 🔧 如果遇到问题

### 问题1：Python未安装
**Mac**:
```bash
brew install python3
```

**Windows**:
从官网下载Python 3.6+

**Linux**:
```bash
sudo apt-get install python3
```

### 问题2：依赖未安装
```bash
pip3 install requests
```

### 问题3：认证信息错误
重新运行设置脚本：
```bash
python3 setup_auth.py
```

---

## 📝 获取认证信息步骤

1. 打开Chrome浏览器
2. 访问 https://v2.aicodee.com/console/topup
3. 按F12打开开发者工具
4. 切换到Network标签
5. 刷新页面
6. 找到API请求（如 `/api/user/info`）
7. 查看请求头中的Authorization
8. 复制值（格式：`Bearer xxxxxxxx`）

---

## 💡 日常使用

### 运行监控
```bash
python3 simple_monitor.py
```

### 快速启动
```bash
python3 快速启动.py
```

### 检查安装
```bash
python3 install.py
```

---

## 🎯 创建快捷方式

### Mac/Linux
```bash
echo 'python3 /path/to/api-usage-monitor/simple_monitor.py' > ~/check_usage.sh
chmod +x ~/check_usage.sh
```

### Windows
创建 `check_usage.bat` 文件，内容：
```batch
python C:\path\to\api-usage-monitor\simple_monitor.py
```

---

## 📊 预期输出

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

## 📞 需要帮助？

查看以下文档：
- `README.md` - 项目说明
- `INSTALL.md` - 详细安装说明
- `新版本使用说明.md` - 详细使用说明

---

**提示**：简单3步，即刻使用！
