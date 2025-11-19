# OB_WiFiQuery
# 欧本 MIFI 流量监控
原作者：https://github.com/lgz666/OB_WiFiQuery
基于 GitHub Actions 的欧本 MIFI 设备流量自动查询和推送系统。

## 功能特点

- 📱 自动查询欧本 MIFI 设备流量使用情况
- ⏰ 定时自动运行（每天早晚8点）
- 🔔 多平台推送通知（微信、钉钉、飞书等）
- 📊 支持多设备同时监控
- 🚀 无需服务器，基于 GitHub Actions

## 快速开始

### 1. Fork 这个仓库

点击右上角的 "Fork" 按钮，将这个仓库复制到你的 GitHub 账户。

### 2. 配置环境变量

进入你的仓库 → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

#### 必需配置：
- **`WIFI_DEV_NOS`**: 你的设备号，多个设备用 `&` 连接
- 
#### 推送配置（至少配置一个）：
- **企业微信**: `WECHAT_ROBOT_WEBHOOK`
- **WxPusher** (推荐): `WXPUSHER_APP_TOKEN` + `WXPUSHER_UIDS`
- **Server酱**: `SERVERJANG_SCKEY`
- **Bark**: `BARK_PUSH_URL`
- **PushPlus**: `PUSHPLUS_TOKEN`
- **钉钉**: `DINGTALK_WEBHOOK`
- **飞书**: `FEISHU_WEBHOOK`

### 3. 手动测试

进入 **Actions** 选项卡：
1. 点击 **OB MIFI Traffic Monitor**
2. 点击 **Run workflow**
3. 选择推送模式（simple/full/off）
4. 点击 **Run workflow**

### 4. 查看结果

工作流运行完成后：
- 在 Actions 日志中查看查询结果
- 检查配置的推送渠道是否收到通知

## 详细配置说明

### 设备号获取

设备号通常可以在：
- MIFI 设备背面标签
- 设备管理后台
- 欧本官方APP中查看

### 推送服务配置指南

#### WxPusher（微信推送，推荐）
1. 访问 [WxPusher官网](https://wxpusher.zjiecode.com/)
2. 注册账号并创建应用，获取 `AppToken`
3. 在微信中关注 WxPusher 公众号，获取你的 `UID`
4. 在 Secrets 中配置：
 - `WXPUSHER_APP_TOKEN`: 你的 AppToken
 - `WXPUSHER_UIDS`: 你的 UID（多个用 `&` 连接）

#### 钉钉机器人
1. 在钉钉群 → 设置 → 智能群助手 → 添加机器人 → 自定义
2. 安全设置选择"自定义关键词"，输入"流量"
3. 复制 Webhook URL，配置到 `DINGTALK_WEBHOOK`

#### 企业微信机器人
1. 在企业微信群 → 右键群聊 → 管理聊天 → 添加机器人
2. 复制 Webhook URL，配置到 `WECHAT_ROBOT_WEBHOOK`

### 推送模式说明

- **`simple`** (默认): 精简信息，包含流量概览和设备状态
- **`full`**: 详细信息，包含所有可读字段和流量卡列表
- **`off`**: 关闭推送，仅在日志中显示结果

 ## 版权与声明

### 原始代码归属
- 本项目基于网络公开的欧本 MIFI 查询脚本进行修改和优化
- 原始脚本版权归原作者所有
- 本人仅对代码进行了以下改进：
  - 添加了 GitHub Actions 自动化部署
  - 增加了多平台推送支持
  - 优化了错误处理和日志输出
  - 完善了配置说明文档

### 使用说明
- 本项目仅供学习和交流使用
- 请勿将本项目用于商业用途
- 使用本项目产生的任何后果由使用者自行承担

### 免责声明
- 本项目不保证查询服务的稳定性和准确性
- 欧本 MIFI 官方服务变更可能导致脚本失效
- 请合理使用流量查询功能，避免频繁请求

### 开源协议
本项目采用 MIT 协议开源，详见 [LICENSE](LICENSE) 文件。

---

**致谢**: 感谢原始脚本的作者和所有贡献者。

## 自定义配置

### 修改运行频率

编辑 `.github/workflows/ob-mifi.yml` 文件中的 `schedule` 部分：

```yaml
schedule:
# 每天 UTC 时间 0:00 和 12:00（北京时间 8:00 和 20:00）
- cron: '0 0 * * *'
- cron: '0 12 * * *'

# 其他示例：
# - cron: '0 */6 * * *'      # 每6小时
# - cron: '0 8,20 * * *'     # 每天8点和20点
# - cron: '0 9 * * *'        # 每天9点




