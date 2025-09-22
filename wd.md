# 火币交易Telegram机器人 - 完整文档

## 📋 目录

- [项目概述](#项目概述)
- [功能特性](#功能特性)
- [系统架构](#系统架构)
- [安装部署](#安装部署)
- [配置说明](#配置说明)
- [使用指南](#使用指南)
- [API文档](#api文档)
- [故障排除](#故障排除)
- [开发指南](#开发指南)
- [更新日志](#更新日志)

## 项目概述

火币交易Telegram机器人是一个功能完善的自动化交易系统，集成了火币(HTX)交易所的API，通过Telegram提供便捷的交易操作界面。

### 核心优势

- **模块化设计**: 每个功能独立模块，易于维护和扩展
- **实时数据**: WebSocket推送，毫秒级延迟
- **智能策略**: 基于4小时K线的网格交易
- **安全可靠**: 多重验证，完善的错误处理
- **可视化**: 图表展示，直观易懂

## 功能特性

### 1. 市场数据 💹
- 实时行情监控
- 24小时涨跌统计
- 深度数据查询
- K线图表生成
- WebSocket实时推送
- 市场趋势分析

### 2. 账户管理 💰
- 现货余额查询
- 资产分布可视化
- 总价值计算
- 交易历史记录
- 盈亏统计分析
- 多账户支持

### 3. 网格交易 🎯
- 基于4小时K线高低点
- 自动计算网格区间
- 动态调整订单
- 成交自动补单
- 策略状态保存
- 利润实时统计

### 4. 现货交易 💱
- 限价/市价买卖
- 智能订单验证
- 精度自动处理
- 批量下单支持
- 订单状态跟踪
- 一键撤单

### 5. 监控预警 🔔
- 价格突破提醒
- 成交通知推送
- 异常波动预警
- 自定义预警规则
- 多渠道通知
- 历史预警记录

### 6. 数据分析 📊
- 资产分布饼图
- K线价格走势
- 网格交易可视化
- 交易统计报表
- 盈亏趋势分析
- 性能指标监控

## 系统架构

```
huobi_telegram_bot/
├── api/                    # API接口模块
│   ├── __init__.py
│   ├── auth.py            # 签名认证
│   ├── client.py          # REST客户端
│   └── websocket.py       # WebSocket客户端
│
├── services/              # 业务服务模块
│   ├── __init__.py
│   ├── market.py          # 市场数据服务
│   ├── account.py         # 账户管理服务
│   ├── trading.py         # 交易执行服务
│   ├── monitoring.py      # 监控预警服务
│   └── statistics.py      # 统计分析服务
│
├── strategies/            # 策略模块
│   ├── __init__.py
│   └── grid_trading.py    # 网格交易策略
│
├── bot/                   # Telegram机器人
│   ├── __init__.py
│   ├── handlers.py        # 消息处理器
│   └── keyboards.py       # 键盘布局
│
├── utils/                 # 工具模块
│   ├── __init__.py
│   └── charts.py          # 图表生成
│
├── config.py              # 配置管理
├── main.py                # 主程序入口
├── requirements.txt       # 依赖包
├── .env.example          # 环境变量示例
├── run.sh                # Linux启动脚本
├── run.bat               # Windows启动脚本
├── Dockerfile            # Docker镜像
└── docker-compose.yml    # Docker编排
```

## 安装部署

### 方式一：本地部署

#### 1. 环境要求

- Python 3.8+
- pip包管理器
- Git（可选）

#### 2. 克隆项目

```bash
git clone https://github.com/your-repo/huobi-telegram-bot.git
cd huobi-telegram-bot
```

或者直接下载代码包解压

#### 3. 创建虚拟环境

```bash
# Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

#### 4. 安装依赖

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 5. 配置环境变量

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入您的配置：

```env
# Telegram配置
TELEGRAM_BOT_TOKEN=your_bot_token_here

# 火币API配置
HUOBI_API_KEY=your_api_key_here
HUOBI_SECRET_KEY=your_secret_key_here

# 可选配置
ALLOWED_USERS=123456789,987654321
LOG_LEVEL=INFO
```

#### 6. 运行机器人

```bash
# 直接运行
python main.py

# 或使用启动脚本
chmod +x run.sh
./run.sh

# Windows
run.bat
```

### 方式二：Docker部署

#### 1. 安装Docker

- [Docker官方安装指南](https://docs.docker.com/get-docker/)
- [Docker Compose安装](https://docs.docker.com/compose/install/)

#### 2. 配置环境变量

```bash
cp .env.example .env
# 编辑.env文件
```

#### 3. 构建并运行

```bash
# 构建镜像
docker-compose build

# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

### 方式三：云服务器部署

#### AWS EC2部署

1. 创建EC2实例（推荐t3.small）
2. 安装Python和Git
3. 按照本地部署步骤操作
4. 使用systemd或supervisor管理进程

#### 阿里云ECS部署

1. 创建ECS实例
2. 配置安全组规则
3. 安装依赖环境
4. 部署应用代码
5. 配置自启动

## 配置说明

### 必需配置

| 配置项 | 说明 | 示例 |
|--------|------|------|
| TELEGRAM_BOT_TOKEN | Telegram机器人令牌 | 123456:ABC-DEF... |
| HUOBI_API_KEY | 火币API密钥 | xxxxxxxx-xxxxxxxx-xxxxxxxx-xxxx |
| HUOBI_SECRET_KEY | 火币私钥 | xxxxxxxx-xxxxxxxx-xxxxxxxx-xxxx |

### 可选配置

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| ALLOWED_USERS | 允许使用的用户ID | 空（所有人可用） |
| LOG_LEVEL | 日志级别 | INFO |
| LOG_FILE | 日志文件路径 | logs/bot.log |
| DATABASE_URL | 数据库连接 | sqlite:///data/bot.db |
| REDIS_HOST | Redis主机 | localhost |
| REDIS_PORT | Redis端口 | 6379 |

### 火币API配置

#### 1. 创建API密钥

1. 登录[火币官网](https://www.huobi.com)
2. 进入账户设置 -> API管理
3. 创建新的API密钥
4. 设置权限（建议只开启读取和交易）
5. 绑定IP地址（可选但推荐）

#### 2. 权限设置

- ✅ 读取权限（必须）
- ✅ 交易权限（必须）
- ❌ 提现权限（不需要）

## 使用指南

### 创建Telegram机器人

1. 在Telegram中搜索 @BotFather
2. 发送 `/newbot` 创建新机器人
3. 设置机器人名称和用户名
4. 获取Bot Token
5. 将Token填入配置文件

### 基本命令

| 命令 | 说明 |
|------|------|
| /start | 启动机器人 |
| /help | 显示帮助 |
| /status | 系统状态 |

### 功能使用

#### 1. 查看市场行情

1. 点击 "💹 市场行情"
2. 自动显示默认交易对行情
3. 包含价格、涨跌幅、成交量

#### 2. 查询账户余额

1. 点击 "💰 账户余额"
2. 显示所有币种余额
3. 计算总价值（USDT）

#### 3. 网格交易设置

1. 点击 "🎯 网格交易"
2. 选择交易对
3. 查看4小时K线分析
4. 输入投资金额
5. 确认启动策略

#### 4. 现货交易

1. 点击 "💱 现货交易"
2. 选择交易对
3. 选择买入/卖出
4. 输入价格和数量
5. 确认下单

#### 5. 设置价格预警

1. 选择交易对
2. 设置预警价格
3. 选择预警类型（突破/跌破）
4. 等待触发通知

### 网格交易详解

#### 工作原理

1. **分析K线**: 获取最近30根4小时K线
2. **计算区间**: 找出最高价和最低价
3. **设置网格**: 在区间内平均分布买卖单
4. **自动交易**: 低买高卖，循环套利

#### 参数说明

- **网格数量**: 默认10层，可调整
- **利润率**: 每格0.2%利润
- **投资金额**: 建议100 USDT起

#### 风险控制

- 适合震荡行情
- 单边行情可能亏损
- 建议小额测试
- 定期检查状态

## API文档

### REST API接口

#### 市场数据

```python
# 获取ticker
ticker = client.get_ticker('btcusdt')

# 获取深度
depth = client.get_depth('btcusdt', depth=20)

# 获取K线
klines = client.get_klines('btcusdt', '4hour', 100)
```

#### 账户接口

```python
# 获取余额
balance = client.get_balance()

# 获取账户列表
accounts = client.get_accounts()
```

#### 交易接口

```python
# 限价买入
order_id = client.place_order(
    symbol='btcusdt',
    amount='0.001',
    price='50000',
    order_type='buy-limit'
)

# 撤销订单
client.cancel_order(order_id)
```

### WebSocket订阅

```python
# 订阅ticker
ws_client.subscribe_ticker('btcusdt', callback)

# 订阅深度
ws_client.subscribe_depth('btcusdt', 'step0', callback)

# 订阅K线
ws_client.subscribe_kline('btcusdt', '1min', callback)
```

## 故障排除

### 常见问题

#### 1. 连接失败

**问题**: API连接失败或超时

**解决方案**:
- 检查网络连接
- 验证API密钥是否正确
- 确认IP白名单设置
- 尝试使用VPN或代理

#### 2. 签名错误

**问题**: API签名验证失败

**解决方案**:
- 检查系统时间是否准确
- 确认密钥没有多余空格
- 验证请求参数格式

#### 3. 下单失败

**问题**: 订单提交失败

**解决方案**:
- 检查余额是否充足
- 验证交易对是否正确
- 确认价格和数量精度
- 查看最小下单限制

#### 4. WebSocket断开

**问题**: WebSocket频繁断开

**解决方案**:
- 检查网络稳定性
- 增加重连间隔
- 减少订阅数量
- 使用心跳保活

### 错误代码

| 错误代码 | 说明 | 解决方法 |
|----------|------|----------|
| invalid-parameter | 参数错误 | 检查参数格式 |
| invalid-sign | 签名错误 | 验证密钥和时间 |
| account-frozen | 账户冻结 | 联系客服 |
| insufficient-balance | 余额不足 | 充值或减少数量 |
| order-limitorder-not-supported | 不支持限价单 | 使用市价单 |
| market-order-not-supported | 不支持市价单 | 使用限价单 |

### 日志查看

```bash
# 查看实时日志
tail -f logs/bot.log

# 查看错误日志
grep ERROR logs/bot.log

# 查看特定日期
grep "2024-01-15" logs/bot.log
```

## 开发指南

### 环境设置

```bash
# 安装开发依赖
pip install -r requirements-dev.txt

# 运行测试
pytest tests/

# 代码检查
flake8 .
black .
```

### 添加新功能

1. 在相应服务模块添加方法
2. 在handlers.py添加处理器
3. 更新keyboards.py添加按钮
4. 编写单元测试
5. 更新文档

### 代码规范

- 遵循PEP 8规范
- 使用类型注解
- 编写文档字符串
- 添加适当的日志
- 处理所有异常

### 提交规范

```bash
# 功能添加
git commit -m "feat: 添加止损功能"

# 错误修复
git commit -m "fix: 修复余额显示错误"

# 文档更新
git commit -m "docs: 更新使用说明"

# 性能优化
git commit -m "perf: 优化数据库查询"
```

## 安全建议

### API安全

1. **限制权限**: 只开启必要的API权限
2. **IP白名单**: 绑定服务器IP
3. **密钥管理**: 使用环境变量存储
4. **定期更换**: 每3个月更换一次密钥

### 交易安全

1. **小额测试**: 新策略先小额测试
2. **止损设置**: 设置合理的止损点
3. **风险控制**: 不要投入全部资金
4. **定期检查**: 每日查看策略状态

### 服务器安全

1. **防火墙**: 只开放必要端口
2. **SSL证书**: 使用HTTPS通信
3. **定期更新**: 及时更新系统和依赖
4. **备份数据**: 定期备份重要数据

## 性能优化

### 数据库优化

- 使用索引提升查询速度
- 定期清理历史数据
- 使用连接池
- 批量操作减少IO

### 缓存策略

- Redis缓存热点数据
- 本地缓存静态信息
- 合理设置过期时间
- 避免缓存雪崩

### 并发处理

- 使用异步IO
- 线程池处理任务
- 消息队列解耦
- 限流保护

## 监控运维

### 健康检查

```python
# 检查API连接
def check_api_health():
    try:
        timestamp = client.get_timestamp()
        return timestamp > 0
    except:
        return False

# 检查数据库
def check_db_health():
    try:
        # 执行简单查询
        return True
    except:
        return False
```

### 性能监控

- CPU使用率
- 内存占用
- 网络延迟
- API调用频率
- 错误率统计

### 告警设置

- API连接异常
- 余额异常变动
- 策略异常停止
- 服务器资源告警

## 更新日志

### v1.0.0 (2024-01-15)

#### 新功能
- ✨ 实现基础交易功能
- ✨ 添加网格交易策略
- ✨ WebSocket实时数据
- ✨ 价格预警功能
- ✨ 图表可视化

#### 改进
- 🎨 优化代码结构
- ⚡ 提升响应速度
- 🔒 增强安全性

#### 修复
- 🐛 修复余额显示问题
- 🐛 修复订单精度错误
- 🐛 修复WebSocket重连

### 开发计划

#### v1.1.0 (计划中)
- [ ] 添加更多交易策略
- [ ] 支持合约交易
- [ ] 多语言支持
- [ ] Web管理界面
- [ ] 自动报表生成

#### v1.2.0 (规划中)
- [ ] AI辅助交易
- [ ] 社交跟单功能
- [ ] 风险评估系统
- [ ] 回测功能
- [ ] 云端同步

## 社区支持

### 官方渠道

- GitHub: [项目地址](https://github.com/your-repo)
- Telegram群: [@huobi_bot_community](https://t.me/huobi_bot_community)
- 邮箱: support@example.com

### 贡献指南

欢迎提交Issue和Pull Request！

1. Fork项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request

### 赞助支持

如果这个项目对您有帮助，欢迎赞助支持开发：

- BTC: bc1qxxxxxxxxxx
- ETH: 0xxxxxxxxxxx
- USDT(TRC20): Txxxxxxxxxx

## 免责声明

⚠️ **风险提示**

1. 本软件仅供学习交流使用
2. 虚拟货币交易风险极高
3. 使用本软件产生的盈亏自负
4. 请遵守当地法律法规
5. 开发者不承担任何责任

## 许可证

MIT License

Copyright (c) 2024 Huobi Trading Bot

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

📝 **文档版本**: v1.0.0  
📅 **更新时间**: 2024-01-15  
👨‍💻 **维护者**: Development Team