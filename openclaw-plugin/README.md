# OpenClaw 用量监控 Hook 插件

OpenClaw 插件，用于在每条 Telegram 回复末尾自动追加 API 用量信息。

## 效果

每条 AI 回复末尾会自动附带用量提示：

```
你的回复内容...

> _📊 剩余$25.40（85%），距离额度重置剩余2小时43分。套餐剩余16天，至 05/22/2026, 10:30 AM_
```

## 安装

1. 将 `openclaw-plugin` 目录复制到 `~/.openclaw/extensions/aicodee-usage-hook/`
2. 在 `~/.openclaw/openclaw.json` 中添加插件配置：

```json
{
  "plugins": {
    "allow": ["aicodee-usage-hook"],
    "entries": {
      "aicodee-usage-hook": {
        "enabled": true,
        "hooks": {
          "allowPromptInjection": true,
          "allowConversationAccess": true
        }
      }
    }
  }
}
```

3. 在 Telegram channel 配置中关闭流式预览（**关键步骤**）：

```json
{
  "channels": {
    "telegram": {
      "streaming": { "mode": "off" }
    }
  }
}
```

4. 重启 Gateway：`openclaw gateway restart`

## 工作原理

插件通过 `message_sending` hook 拦截每条 outgoing 消息，读取 `~/.openclaw/scripts/usage_cache.txt` 中的用量数据，追加到消息末尾。

## 重要：为什么必须关闭 Telegram 流式预览

**问题**：Telegram 默认启用流式预览模式（`streaming: "partial"`），AI 回复时通过 `editMessageTelegram` 实时编辑同一条消息实现打字效果。这个编辑过程完全绕过了 `deliverReplies` 函数，而 `message_sending` hook 恰恰是在 `deliverReplies` 内部触发的，因此 hook 永远不会被调用。

**解决方案**：在 `openclaw.json` 的 `channels.telegram` 配置中添加 `streaming: { "mode": "off" }` 关闭流式预览，使所有回复走 `deliverReplies` 标准发送路径，这样 `message_sending` hook 就能正常拦截每条消息并追加用量后缀。

**代价**：Telegram 不再有实时打字流式效果，回复会一次性完整显示。

## 依赖

- `~/.openclaw/scripts/usage_cache.txt` — 由 `api-usage-monitor` 的 Python 脚本生成
- 需要配合定时任务定期更新 `usage_cache.txt`
