# 📤 GitHub上传指南

## 🎯 上传步骤

### 第1步：初始化Git仓库
```bash
cd ~/Desktop/ApiUsageMonitor
git init
```

### 第2步：添加文件到Git
```bash
git add .
```

### 第3步：提交更改
```bash
git commit -m "初始提交：API用量监控工具 - 一键安装版"
```

### 第4步：创建GitHub仓库
1. 访问 https://github.com
2. 点击右上角 "+" → "New repository"
3. 填写仓库名称（如：api-usage-monitor）
4. 填写描述
5. 选择 Public 或 Private
6. 点击 "Create repository"

### 第5步：连接远程仓库
```bash
git remote add origin https://github.com/your-username/api-usage-monitor.git
```

### 第6步：推送代码
```bash
git branch -M main
git push -u origin main
```

---

## 📋 上传前检查清单

### 确保以下文件已准备好：
- [ ] `simple_monitor.py` - 主监控脚本
- [ ] `setup_auth.py` - 认证信息设置
- [ ] `快速启动.py` - 快速启动
- [ ] `install.py` - 一键安装程序
- [ ] `README.md` - 项目说明
- [ ] `INSTALL.md` - 安装说明
- [ ] `QUICK_START.md` - 快速开始指南
- [ ] `LICENSE` - 许可证文件
- [ ] `.gitignore` - Git忽略文件

### 确保以下文件未上传：
- [ ] `auth_info.json` - 认证信息（敏感）
- [ ] `usage_cache.json` - 缓存数据
- [ ] `__pycache__/` - Python缓存

---

## 🎯 其他电脑使用方法（超简单）

### 方法1：一键安装（推荐）
```bash
git clone https://github.com/your-username/api-usage-monitor.git
cd api-usage-monitor
python3 install.py
```

安装程序会自动完成所有配置！

### 方法2：手动安装
```bash
git clone https://github.com/your-username/api-usage-monitor.git
cd api-usage-monitor
python3 setup_auth.py
python3 simple_monitor.py
```

---

## 📊 仓库结构建议

```
api-usage-monitor/
├── README.md
├── INSTALL.md
├── QUICK_START.md
├── LICENSE
├── .gitignore
├── install.py
├── simple_monitor.py
├── setup_auth.py
├── 快速启动.py
├── api_direct_monitor.py
├── 对比测试.py
├── 新版本使用说明.md
├── 新旧版本对比.md
├── 最新测试报告.md
└── 效果演示总结.md
```

---

## 💡 其他电脑的使用流程

### 超简单流程（3步）：
1. **克隆仓库**：`git clone https://github.com/your-username/api-usage-monitor.git`
2. **进入目录**：`cd api-usage-monitor`
3. **一键安装**：`python3 install.py`

### 安装完成后：
```bash
python3 simple_monitor.py
```

---

## 🔧 常见问题

### 问题1：如何更新代码？
```bash
# 修改文件后
git add .
git commit -m "更新说明"
git push
```

### 问题2：如何创建新分支？
```bash
git checkout -b feature/新功能
# 开发完成后
git push -u origin feature/新功能
```

### 问题3：如何查看提交历史？
```bash
git log
```

---

## 📝 提交信息规范

### 提交信息格式
```
<类型>: <描述>

<详细说明>
```

### 类型说明
- `feat`: 新功能
- `fix`: 修复bug
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 重构
- `test`: 测试相关
- `chore`: 构建/工具相关

### 示例
```
feat: 添加一键安装程序

- 实现自动安装和配置
- 支持跨平台使用
- 添加快捷方式创建
```

---

## 🎯 总结

**其他电脑使用超简单**：
1. 克隆仓库
2. 运行 `python3 install.py`
3. 完成！

**一键安装，即刻使用！** 🎉

---

**上传完成时间**: [当前时间]
**上传人员**: [你的名字]
**版本**: v1.0
