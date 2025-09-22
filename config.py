# ============ config.py ============
"""
配置文件 - 所有配置项集中管理
"""
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


class Config:
    """配置类"""

    # ========== Telegram配置 ==========
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    ALLOWED_USERS = os.getenv('ALLOWED_USERS', '').split(',') if os.getenv('ALLOWED_USERS') else []

    # ========== 火币API配置 ==========
    HUOBI_API_KEY = os.getenv('HUOBI_API_KEY')
    HUOBI_SECRET_KEY = os.getenv('HUOBI_SECRET_KEY')
    HUOBI_BASE_URL = os.getenv('HUOBI_BASE_URL', 'https://api.huobi.pro')
    HUOBI_WS_URL = os.getenv('HUOBI_WS_URL', 'wss://api.huobi.pro/ws')

    # ========== 交易配置 ==========
    # 默认监控的交易对
    DEFAULT_SYMBOLS = ['btcusdt', 'ethusdt', 'bnbusdt', 'dogeusdt']

    # 网格交易配置
    GRID_LEVELS = 10  # 网格层数
    GRID_PROFIT_RATE = 0.002  # 每格利润率 0.2%
    GRID_MIN_AMOUNT = 10  # 最小交易金额 USDT

    # 交易限制
    MAX_ORDER_PER_SYMBOL = 50  # 每个交易对最大挂单数
    MIN_ORDER_INTERVAL = 1  # 最小下单间隔(秒)

    # ========== 系统配置 ==========
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/bot.log')
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///data/bot.db')

    # Redis配置（可选）
    REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
    REDIS_DB = int(os.getenv('REDIS_DB', 0))
    REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', None)

    # ========== 监控配置 ==========
    PRICE_ALERT_INTERVAL = 60  # 价格预警检查间隔(秒)
    MONITOR_INTERVAL = 5  # 市场监控间隔(秒)

    # ========== API限制配置 ==========
    API_RATE_LIMIT = {
        'rest': 100,  # REST API每2秒限制
        'ws': 10,  # WebSocket连接数限制
    }

    @classmethod
    def validate(cls):
        """验证配置"""
        errors = []

        if not cls.TELEGRAM_BOT_TOKEN:
            errors.append("TELEGRAM_BOT_TOKEN is required")

        if not cls.HUOBI_API_KEY:
            errors.append("HUOBI_API_KEY is required")

        if not cls.HUOBI_SECRET_KEY:
            errors.append("HUOBI_SECRET_KEY is required")

        if errors:
            raise ValueError(f"Configuration errors: {', '.join(errors)}")

        return True


# ============ .env.example ============
"""
# Telegram Bot配置
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
# 允许使用的用户ID，多个用逗号分隔，留空则允许所有用户
ALLOWED_USERS=123456789,987654321

# 火币API配置
HUOBI_API_KEY=your_huobi_api_key_here
HUOBI_SECRET_KEY=your_huobi_secret_key_here
# API地址（可选，默认值即可）
HUOBI_BASE_URL=https://api.huobi.pro
HUOBI_WS_URL=wss://api.huobi.pro/ws

# 日志配置
LOG_LEVEL=INFO
LOG_FILE=logs/bot.log

# 数据库配置
DATABASE_URL=sqlite:///data/bot.db

# Redis配置（可选）
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=

# 注意事项：
# 1. 请将此文件复制为 .env 并填入实际的配置值
# 2. 不要将 .env 文件提交到版本控制系统
# 3. 确保 API 密钥的安全性
"""

# ============ requirements.txt ============
"""
# Telegram Bot
python-telegram-bot==20.3

# 环境变量
python-dotenv==1.0.0

# HTTP请求
requests==2.31.0
aiohttp==3.8.5

# WebSocket
websocket-client==1.6.1

# 数据处理
pandas==2.0.3
numpy==1.24.3

# 图表生成
matplotlib==3.7.1
pillow==10.0.0

# 数据库
sqlalchemy==2.0.19
redis==4.6.0

# 工具库
pytz==2023.3
python-dateutil==2.8.2

# 日志
loguru==0.7.0
"""

# ============ setup.py ============
"""
from setuptools import setup, find_packages

setup(
    name='huobi-telegram-bot',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'python-telegram-bot>=20.3',
        'python-dotenv>=1.0.0',
        'requests>=2.31.0',
        'websocket-client>=1.6.1',
        'pandas>=2.0.3',
        'matplotlib>=3.7.1',
        'sqlalchemy>=2.0.19',
    ],
    python_requires='>=3.8',
    author='Your Name',
    description='Huobi Trading Telegram Bot',
)
"""