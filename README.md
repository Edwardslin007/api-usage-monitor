# 🎯 API用量监控工具

[![Python](https://img.shields.io/badge/Python-3.6%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Mac%2FWindows%2FLinux-green.svg)]()

## 📋 项目介绍

这是一个**API用量监控工具**，可以自动获取并显示你的API使用情况。只需运行一个命令，即可实时查看剩余额度、使用百分比、套餐到期时间等信息。

### 🎯 功能特点

✅ **一键运行** - 只需 `python3 simple_monitor.py`  
✅ **自动获取认证** - 从Chrome浏览器自动读取认证信息  
✅ **真实数据** - 直接调用API获取真实用量数据  
✅ **无需打开网页** - 完全静默运行  
✅ **跨平台** - 支持Mac、Windows、Linux  

### 📊 输出示例

```
剩余$24.40（81.3%），距离额度重置剩余1小时59分。套餐剩余16天，至 05/22/2026, 10:30:26 AM
```

---

## 🚀 从零开始使用指南

### 第1步：安装Python

#### Mac/Linux
```bash
# 使用Homebrew安装
brew install python3

# 或者从官网下载：https://www.python.org/downloads/
```

#### Windows
1. 访问 https://www.python.org/downloads/
2. 下载Python 3.6或更高版本
3. 安装时勾选"Add Python to PATH"

#### 验证安装
```bash
python3 --version
# 应该显示 Python 3.6.x 或更高版本
```

### 第2步：安装依赖包

```bash
pip3 install requests browser_cookie3
```

#### 如果遇到权限问题
```bash
# Mac/Linux
sudo pip3 install requests browser_cookie3

# Windows（以管理员身份运行CMD）
pip install requests browser_cookie3
```

### 第3步：下载项目

```bash
# 方式1：克隆仓库（推荐）
git clone https://github.com/your-username/api-usage-monitor.git
cd api-usage-monitor

# 方式2：下载ZIP
# 从GitHub页面点击 "Code" → "Download ZIP"
# 解压后进入文件夹
```

### 第4步：准备Chrome浏览器

1. **打开Chrome浏览器**
2. **访问并登录**：https://v2.aicodee.com/console/topup
3. **保持页面打开状态**

#### 启用Chrome调试端口（重要！）

关闭Chrome浏览器，然后使用以下命令重新启动：

**Mac/Linux:**
```bash
open -a "Google Chrome" --args --remote-debugging-port=9222
```

**Windows:**
```batch
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222
```

#### 验证调试端口
```bash
curl -s http://localhost:9222/json/version
# 如果返回JSON信息，说明配置成功
```

### 第5步：运行监控工具

```bash
python3 simple_monitor.py
```

**完成！** 🎉

---

## 🔧 底层原理详解

### 1. 整体架构

```
┌─────────────────────────────────────────────────────────────┐
│                    工作流程                                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. 从Chrome浏览器读取cookies                               │
│     ↓                                                       │
│  2. 通过Chrome DevTools Protocol获取用户ID                  │
│     ↓                                                       │
│  3. 调用API获取订阅数据                                     │
│     ↓                                                       │
│  4. 解析数据并计算用量信息                                  │
│     ↓                                                       │
│  5. 格式化输出                                              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 2. 认证信息获取原理

#### 2.1 从Chrome读取Cookies

脚本使用 `browser_cookie3` 库直接从Chrome的Cookie数据库中读取cookies：

```python
import browser_cookie3

# 读取v2.aicodee.com的cookies
cj = browser_cookie3.chrome(domain_name='v2.aicodee.com')
cookies_dict = {}
for cookie in cj:
    cookies_dict[cookie.name] = cookie.value
```

**原理**：
- Chrome将cookies存储在SQLite数据库中
- 数据库位置：`~/Library/Application Support/Google/Chrome/Default/Cookies`（Mac）
- `browser_cookie3`库可以解密并读取这些cookies

#### 2.2 通过Chrome DevTools Protocol获取用户ID

由于用户ID存储在localStorage中，脚本使用Chrome DevTools Protocol来获取：

```javascript
// Node.js脚本
const http = require('http');
const WebSocket = require('ws');

// 连接到Chrome调试端口
http.get('http://localhost:9222/json', (res) => {
    // 获取页面列表
    // 找到目标页面
    // 通过WebSocket连接
    // 执行JavaScript获取localStorage
});
```

**原理**：
- Chrome调试端口（9222）提供HTTP和WebSocket接口
- 通过WebSocket可以执行JavaScript代码
- `localStorage.getItem('user')` 获取用户信息

### 3. API调用原理

#### 3.1 API端点

脚本调用以下API端点获取数据：

| 端点 | 用途 |
|------|------|
| `/api/user/self` | 获取用户信息 |
| `/api/subscription/self` | 获取订阅信息 |

#### 3.2 请求头

```python
headers = {
    'User-Agent': 'Mozilla/5.0',
    'Accept': 'application/json',
    'New-Api-User': str(user_id),  # 用户ID
}
```

**关键点**：
- `New-Api-User` header 必须包含用户ID
- Cookies用于身份验证

### 4. 数据解析原理

#### 4.1 订阅数据结构

```json
{
  "subscription": {
    "id": 3369,
    "amount_total": 15000000,    // 总额度（单位）
    "amount_used": 2800000,      // 已用额度（单位）
    "end_time": 1779417026,      // 结束时间（时间戳）
    "next_reset_time": 1777995026  // 下次重置时间（时间戳）
  }
}
```

#### 4.2 额度转换

```python
# 单位转换：1 unit = $0.000002
# 15000000 units = $30.00
total_usd = total_units * 0.000002
```

#### 4.3 时间计算

```python
# 计算剩余天数
remaining_days = (end_time - datetime.now()).days

# 计算距离重置的时间
time_to_reset = next_reset - now
hours = time_to_reset.seconds // 3600
minutes = (time_to_reset.seconds % 3600) // 60
```

### 5. 输出格式化

```python
message = (
    f"剩余${remaining_usd:.2f}（{remaining_percent:.1f}%），"
    f"距离额度重置剩余{hours}小时{minutes}分。"
    f"套餐剩余{remaining_days}天，至 {reset_date_str}"
)
```

---

## 📁 项目结构

```
api-usage-monitor/
├── simple_monitor.py          # 主监控脚本（一键运行）
├── install.py                 # 一键安装程序
├── setup_auth.py              # 认证信息设置（备选）
├── api_direct_monitor.py      # API直接调用版本
├── 快速启动.py                # 快速启动
├── 对比测试.py                # 新旧版本对比测试
├── README.md                  # 项目说明（本文件）
├── INSTALL.md                 # 安装说明
├── QUICK_START.md             # 快速开始指南
├── GITHUB_UPLOAD_GUIDE.md     # GitHub上传指南
├── 新版本使用说明.md          # 详细使用说明
├── 新旧版本对比.md            # 新旧版本对比
├── 最新测试报告.md            # 测试报告
├── 效果演示总结.md            # 效果演示总结
├── .gitignore                 # Git忽略文件
├── LICENSE                    # MIT许可证
└── openclaw-plugin/           # OpenClaw Telegram 用量 Hook 插件
    ├── index.js               # 插件主文件
    ├── openclaw.plugin.json   # 插件清单
    ├── package.json           # 包配置
    └── README.md              # 插件说明（含踩坑记录）
```

---

## 🔧 常见问题

### 问题1：提示"无法从浏览器获取cookies"

**原因**：Chrome浏览器未打开或未登录

**解决方案**：
1. 打开Chrome浏览器
2. 登录到 https://v2.aicodee.com/console/topup
3. 保持页面打开状态

### 问题2：提示"无法获取用户ID"

**原因**：Chrome调试端口未开启

**解决方案**：
1. 关闭Chrome浏览器
2. 使用以下命令重新启动：
   ```bash
   open -a "Google Chrome" --args --remote-debugging-port=9222
   ```

### 问题3：提示"ModuleNotFoundError: No module named 'browser_cookie3'"

**原因**：未安装browser_cookie3库

**解决方案**：
```bash
pip3 install browser_cookie3
```

### 问题4：Windows上无法运行

**解决方案**：
1. 确保Python已添加到PATH
2. 使用 `python` 而不是 `python3`
3. 以管理员身份运行CMD

---

## 📊 性能指标

| 指标 | 数值 |
|------|------|
| 执行时间 | 0.2-0.5秒 |
| 网络请求 | 2-3次 |
| 内存占用 | <50MB |
| CPU占用 | <1% |

---

## 🤝 贡献

欢迎贡献代码！请遵循以下步骤：

1. Fork 本仓库
2. 创建你的分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建一个 Pull Request

---

## 📄 许可证

本项目使用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

---

## 🔌 OpenClaw Telegram 插件

本项目还包含一个 OpenClaw 插件，可以在 Telegram 每条 AI 回复末尾自动追加用量信息。

### 效果

```
你的回复内容...

> _📊 剩余$25.40（85%），距离额度重置剩余2小时43分。套餐剩余16天，至 05/22/2026, 10:30 AM_
```

### 安装

1. 将 `openclaw-plugin/` 目录复制到 `~/.openclaw/extensions/aicodee-usage-hook/`
2. 在 `~/.openclaw/openclaw.json` 中启用插件（详见 [openclaw-plugin/README.md](openclaw-plugin/README.md)）
3. **关键**：在 Telegram 配置中关闭流式预览：`"streaming": { "mode": "off" }`
4. 重启 Gateway：`openclaw gateway restart`

### 踩坑记录

**问题**：`message_sending` hook 永远不会触发。

**根因**：Telegram 默认启用流式预览模式（`streaming: "partial"`），AI 回复通过 `editMessageTelegram` 实时编辑同一条消息，完全绕过 `deliverReplies` 函数。而 `message_sending` hook 在 `deliverReplies` 内部触发，所以永远不会被调用。

**解决**：关闭流式预览（`streaming: { "mode": "off" }`），使回复走标准 `deliverReplies` 路径。

**代价**：Telegram 不再有打字流式效果，回复一次性完整显示。

详细说明见 [openclaw-plugin/README.md](openclaw-plugin/README.md)。

---

## 📞 联系方式

- **作者**: [你的名字]
- **邮箱**: [你的邮箱]
- **GitHub**: [你的GitHub主页]

---

## 🙏 致谢

感谢所有为这个项目做出贡献的人！

---

**提示**：一键运行，即刻使用！
