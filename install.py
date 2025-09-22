#!/usr/bin/env python3
"""
火币交易Telegram机器人 - 一键部署脚本
运行此脚本将自动创建完整的项目结构和所有必要文件
"""

import os
import sys
import base64
import json
from pathlib import Path

# 项目名称
PROJECT_NAME = "huobi_telegram_bot"

# 文件内容定义
FILES = {
    # ============ 配置文件 ============
    "config.py": '''"""
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
    DEFAULT_SYMBOLS = ['btcusdt', 'ethusdt', 'bnbusdt', 'dogeusdt']
    GRID_LEVELS = 10
    GRID_PROFIT_RATE = 0.002
    GRID_MIN_AMOUNT = 10

    # ========== 系统配置 ==========
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/bot.log')
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///data/bot.db')

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
''',

    ".env.example": '''# Telegram Bot配置
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
# 允许使用的用户ID，多个用逗号分隔，留空则允许所有用户
ALLOWED_USERS=

# 火币API配置
HUOBI_API_KEY=your_huobi_api_key_here
HUOBI_SECRET_KEY=your_huobi_secret_key_here

# 日志配置
LOG_LEVEL=INFO
LOG_FILE=logs/bot.log

# 数据库配置
DATABASE_URL=sqlite:///data/bot.db
''',

    "requirements.txt": '''# Telegram Bot
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

# 工具库
pytz==2023.3
python-dateutil==2.8.2
''',

    # ============ API模块 ============
    "api/__init__.py": '''"""
API模块初始化
"""
from .auth import HuobiAuth
from .client import HuobiClient

__all__ = ['HuobiAuth', 'HuobiClient']
''',

    "api/auth.py": '''"""
火币API签名认证模块
"""
import hmac
import hashlib
import base64
from datetime import datetime
from urllib.parse import urlencode, quote
import logging

logger = logging.getLogger(__name__)

class HuobiAuth:
    """火币API认证类"""

    def __init__(self, api_key: str, secret_key: str):
        self.api_key = api_key
        self.secret_key = secret_key

    def generate_signature(self, method: str, url: str, params: dict = None) -> dict:
        """生成API签名"""
        timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')

        params_to_sign = {
            'AccessKeyId': self.api_key,
            'SignatureMethod': 'HmacSHA256',
            'SignatureVersion': '2',
            'Timestamp': timestamp,
        }

        if params:
            params_to_sign.update(params)

        sorted_params = sorted(params_to_sign.items())
        encoded_params = urlencode(sorted_params)

        url_without_protocol = url.replace('https://', '').replace('http://', '')
        parts = url_without_protocol.split('/')
        host = parts[0]
        path = '/' + '/'.join(parts[1:]) if len(parts) > 1 else '/'

        payload = f'{method}\\n{host}\\n{path}\\n{encoded_params}'

        signature = base64.b64encode(
            hmac.new(
                self.secret_key.encode('utf-8'),
                payload.encode('utf-8'),
                hashlib.sha256
            ).digest()
        ).decode('utf-8')

        params_to_sign['Signature'] = signature

        return params_to_sign
''',

    "api/client.py": '''"""
火币REST API客户端
"""
import requests
import json
import logging
import time
from typing import Dict, Any, Optional, List
from .auth import HuobiAuth

logger = logging.getLogger(__name__)

class HuobiClient:
    """火币API客户端"""

    def __init__(self, api_key: str, secret_key: str, base_url: str = 'https://api.huobi.pro'):
        self.api_key = api_key
        self.secret_key = secret_key
        self.base_url = base_url
        self.auth = HuobiAuth(api_key, secret_key)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0',
            'Content-Type': 'application/json'
        })
        self.account_id = None
        self._last_request_time = 0
        self._request_interval = 0.02

    def _request(self, method: str, path: str, params: Dict = None, 
                auth_required: bool = False) -> Dict:
        """发送HTTP请求"""
        current_time = time.time()
        time_diff = current_time - self._last_request_time
        if time_diff < self._request_interval:
            time.sleep(self._request_interval - time_diff)

        url = f"{self.base_url}{path}"

        try:
            if auth_required:
                auth_params = self.auth.generate_signature(method, url, params if method == 'GET' else None)

                if method == 'GET':
                    response = self.session.get(url, params=auth_params, timeout=10)
                else:
                    response = self.session.post(
                        url, 
                        params=auth_params,
                        data=json.dumps(params) if params else None,
                        timeout=10
                    )
            else:
                if method == 'GET':
                    response = self.session.get(url, params=params, timeout=10)
                else:
                    response = self.session.post(url, json=params, timeout=10)

            self._last_request_time = time.time()
            response.raise_for_status()
            data = response.json()

            if data.get('status') == 'error':
                error_msg = f"API Error: {data.get('err-code', 'Unknown')} - {data.get('err-msg', 'No message')}"
                logger.error(error_msg)
                raise Exception(error_msg)

            return data

        except Exception as e:
            logger.error(f"Request failed: {e}")
            raise

    def get_symbols(self) -> List[Dict]:
        """获取所有交易对信息"""
        response = self._request('GET', '/v1/common/symbols')
        return response.get('data', [])

    def get_ticker(self, symbol: str) -> Dict:
        """获取最新ticker"""
        response = self._request('GET', '/market/detail/merged', {'symbol': symbol})
        return response.get('tick', {})

    def get_klines(self, symbol: str, period: str, size: int = 200) -> List:
        """获取K线数据"""
        params = {
            'symbol': symbol,
            'period': period,
            'size': size
        }
        response = self._request('GET', '/market/history/kline', params)
        return response.get('data', [])

    def get_accounts(self) -> List[Dict]:
        """获取账户列表"""
        response = self._request('GET', '/v1/account/accounts', auth_required=True)
        return response.get('data', [])

    def get_balance(self, account_id: int = None) -> Dict:
        """获取账户余额"""
        if not account_id:
            accounts = self.get_accounts()
            for account in accounts:
                if account['type'] == 'spot' and account['state'] == 'working':
                    account_id = account['id']
                    break

        response = self._request('GET', f'/v1/account/accounts/{account_id}/balance', auth_required=True)
        return response.get('data', {})

    def place_order(self, symbol: str, amount: str, price: str = None, 
                   order_type: str = 'buy-limit', client_order_id: str = None) -> str:
        """下单"""
        if not self.account_id:
            accounts = self.get_accounts()
            self.account_id = next(acc['id'] for acc in accounts if acc['type'] == 'spot')

        params = {
            'account-id': str(self.account_id),
            'symbol': symbol,
            'type': order_type,
            'amount': amount
        }

        if 'limit' in order_type and price:
            params['price'] = price

        response = self._request('POST', '/v1/order/orders/place', params, auth_required=True)
        return response.get('data', '')
''',

    # ============ 主程序 ============
    "main.py": '''"""
火币交易Telegram机器人 - 主程序
"""
import logging
import sys
import os
from datetime import datetime

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters
)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import Config
from bot.handlers import BotHandlers

# 配置日志
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

class HuobiTradingBot:
    """火币交易机器人主类"""

    def __init__(self):
        self.config = Config()
        self.handlers = None
        self.app = None

    def setup_handlers(self):
        """设置消息处理器"""
        self.handlers = BotHandlers()

        self.app.add_handler(CommandHandler("start", self.handlers.start))
        self.app.add_handler(CommandHandler("help", self.handlers.help))

        self.app.add_handler(CallbackQueryHandler(self.handlers.handle_callback_query))

        self.app.add_handler(MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            self.handlers.handle_text_message
        ))

    async def error_handler(self, update: Update, context):
        """错误处理器"""
        logger.error(f"Update {update} caused error {context.error}")

        if update and update.effective_message:
            try:
                await update.effective_message.reply_text(
                    "❌ 发生错误，请稍后重试"
                )
            except:
                pass

    def run(self):
        """运行机器人"""
        try:
            self.config.validate()

            self.app = Application.builder().token(self.config.TELEGRAM_BOT_TOKEN).build()

            self.setup_handlers()
            self.app.add_error_handler(self.error_handler)

            logger.info("火币交易机器人启动中...")

            self.app.run_polling(
                allowed_updates=Update.ALL_TYPES,
                drop_pending_updates=True
            )

        except Exception as e:
            logger.error(f"机器人运行失败: {e}")
            raise

def main():
    """主函数"""
    logger.info("=" * 50)
    logger.info("火币交易Telegram机器人")
    logger.info("版本: 1.0.0")
    logger.info(f"启动时间: {datetime.now()}")
    logger.info("=" * 50)

    bot = HuobiTradingBot()
    bot.run()

if __name__ == '__main__':
    main()
''',

    # ============ 其他必要文件（简化版） ============
    "bot/__init__.py": '''from .handlers import BotHandlers
from .keyboards import Keyboards

__all__ = ['BotHandlers', 'Keyboards']
''',

    "bot/handlers.py": '''"""
Telegram消息处理器
"""
import logging
from telegram import Update
from telegram.ext import ContextTypes
from config import Config
from api.client import HuobiClient

logger = logging.getLogger(__name__)

class BotHandlers:
    def __init__(self):
        self.config = Config()
        self.client = HuobiClient(
            self.config.HUOBI_API_KEY,
            self.config.HUOBI_SECRET_KEY,
            self.config.HUOBI_BASE_URL
        )

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """处理 /start 命令"""
        welcome_text = (
            "🤖 *欢迎使用火币交易机器人*\\n\\n"
            "主要功能：\\n"
            "• 💹 实时行情监控\\n"
            "• 💰 账户余额查询\\n"
            "• 🎯 网格交易策略\\n"
            "• 💱 现货交易下单\\n\\n"
            "/help - 查看帮助"
        )

        await update.message.reply_text(
            welcome_text,
            parse_mode='MarkdownV2'
        )

    async def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """处理 /help 命令"""
        help_text = "使用帮助：\\n/start - 启动机器人\\n/help - 显示帮助"
        await update.message.reply_text(help_text, parse_mode='MarkdownV2')

    async def handle_text_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """处理文本消息"""
        text = update.message.text

        if text == '💹 市场行情':
            await self.handle_market_info(update, context)
        elif text == '💰 账户余额':
            await self.handle_balance(update, context)
        else:
            await update.message.reply_text("请使用命令或按钮选择功能")

    async def handle_market_info(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """处理市场行情查询"""
        try:
            ticker = self.client.get_ticker('btcusdt')
            price = ticker.get('close', 0)
            await update.message.reply_text(f"BTC/USDT 当前价格: ${price:,.2f}")
        except Exception as e:
            logger.error(f"获取行情失败: {e}")
            await update.message.reply_text("❌ 获取行情失败")

    async def handle_balance(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """处理余额查询"""
        try:
            balance = self.client.get_balance()
            total_value = 0
            text = "*账户余额*\\n\\n"

            for item in balance.get('list', [])[:5]:
                if float(item['balance']) > 0:
                    currency = item['currency'].upper()
                    amount = float(item['balance'])
                    text += f"{currency}: {amount:.8f}\\n"

            await update.message.reply_text(text, parse_mode='MarkdownV2')
        except Exception as e:
            logger.error(f"获取余额失败: {e}")
            await update.message.reply_text("❌ 获取余额失败")

    async def handle_callback_query(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """处理回调查询"""
        query = update.callback_query
        await query.answer()
        await query.message.reply_text("功能开发中...")
''',

    "bot/keyboards.py": '''"""
Telegram键盘布局
"""
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup

class Keyboards:
    @staticmethod
    def main_menu():
        """主菜单键盘"""
        keyboard = [
            ['💹 市场行情', '💰 账户余额'],
            ['🎯 网格交易', '💱 现货交易'],
        ]
        return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
'''
}


def create_project():
    """创建项目结构和文件"""
    print("=" * 60)
    print("火币交易Telegram机器人 - 自动部署脚本")
    print("=" * 60)

    # 创建项目根目录
    if os.path.exists(PROJECT_NAME):
        print(f"⚠️  目录 {PROJECT_NAME} 已存在")
        response = input("是否覆盖? (y/n): ")
        if response.lower() != 'y':
            print("❌ 部署已取消")
            return False

    # 创建目录结构
    directories = [
        PROJECT_NAME,
        f"{PROJECT_NAME}/api",
        f"{PROJECT_NAME}/services",
        f"{PROJECT_NAME}/strategies",
        f"{PROJECT_NAME}/bot",
        f"{PROJECT_NAME}/utils",
        f"{PROJECT_NAME}/logs",
        f"{PROJECT_NAME}/data"
    ]

    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ 创建目录: {directory}")

    # 创建文件
    for filepath, content in FILES.items():
        full_path = os.path.join(PROJECT_NAME, filepath)

        # 确保目录存在
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"✅ 创建文件: {filepath}")

    # 创建简化的服务文件（示例）
    service_files = {
        "services/__init__.py": "# Services module",
        "strategies/__init__.py": "# Strategies module",
        "utils/__init__.py": "# Utils module"
    }

    for filepath, content in service_files.items():
        full_path = os.path.join(PROJECT_NAME, filepath)
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)

    # 创建启动脚本
    create_scripts()

    print("\n" + "=" * 60)
    print("✅ 项目创建成功！")
    print("=" * 60)
    print("\n📝 下一步操作：")
    print(f"1. 进入项目目录: cd {PROJECT_NAME}")
    print("2. 复制环境变量: cp .env.example .env")
    print("3. 编辑配置文件: 编辑 .env 文件，填入您的API密钥")
    print("4. 安装依赖包: pip install -r requirements.txt")
    print("5. 运行机器人: python main.py")
    print("\n💡 提示：")
    print("- 请确保已创建Telegram机器人并获取Token")
    print("- 请确保已在火币创建API密钥")
    print("- 建议先用小额资金测试")

    return True


def create_scripts():
    """创建启动脚本"""
    # Linux/Mac启动脚本
    bash_script = '''#!/bin/bash
echo "Starting Huobi Trading Bot..."
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
'''

    with open(f"{PROJECT_NAME}/run.sh", 'w') as f:
        f.write(bash_script)

    os.chmod(f"{PROJECT_NAME}/run.sh", 0o755)

    # Windows启动脚本
    bat_script = '''@echo off
echo Starting Huobi Trading Bot...
python -m venv venv
call venv\\Scripts\\activate.bat
pip install -r requirements.txt
python main.py
pause
'''

    with open(f"{PROJECT_NAME}/run.bat", 'w') as f:
        f.write(bat_script)


if __name__ == "__main__":
    try:
        success = create_project()
        if success:
            print("\n🎉 部署完成！祝您交易顺利！")
    except Exception as e:
        print(f"\n❌ 部署失败: {e}")
        sys.exit(1)