#!/usr/bin/env python3
"""
🤖 火币交易Telegram机器人 - 智能安装配置向导
====================================================
此脚本将帮助您完成：
1. 环境检查和依赖安装
2. 交互式配置向导
3. API连接测试
4. 项目文件生成
5. 自动启动机器人
"""

import os
import sys
import json
import time
import subprocess
import platform
import shutil
from pathlib import Path
from datetime import datetime
import base64
import hashlib
import hmac
from urllib.parse import urlencode


# ANSI颜色代码
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_colored(text, color=Colors.END):
    """打印彩色文本"""
    print(f"{color}{text}{Colors.END}")


def print_header():
    """打印欢迎界面"""
    os.system('cls' if os.name == 'nt' else 'clear')
    print_colored("=" * 70, Colors.CYAN)
    print_colored("         🤖 火币交易 Telegram 机器人 - 智能安装向导", Colors.BOLD)
    print_colored("=" * 70, Colors.CYAN)
    print_colored("         版本: 1.0.0  |  作者: AI Assistant", Colors.GREEN)
    print_colored("=" * 70, Colors.CYAN)
    print()


def check_python_version():
    """检查Python版本"""
    print_colored("🔍 检查Python版本...", Colors.BLUE)
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print_colored(f"❌ Python版本过低: {version.major}.{version.minor}", Colors.FAIL)
        print_colored("   需要Python 3.8或更高版本", Colors.WARNING)
        return False
    print_colored(f"✅ Python版本: {version.major}.{version.minor}.{version.micro}", Colors.GREEN)
    return True


def check_pip():
    """检查pip是否安装"""
    print_colored("🔍 检查pip...", Colors.BLUE)
    try:
        import pip
        print_colored(f"✅ pip已安装", Colors.GREEN)
        return True
    except ImportError:
        print_colored("❌ pip未安装", Colors.FAIL)
        return False


def install_dependencies():
    """安装依赖包"""
    print_colored("\n📦 安装依赖包...", Colors.BLUE)

    dependencies = [
        "python-telegram-bot==20.3",
        "python-dotenv==1.0.0",
        "requests==2.31.0",
        "aiohttp==3.8.5",
        "websocket-client==1.6.1",
        "pandas==2.0.3",
        "numpy==1.24.3",
        "matplotlib==3.7.1",
        "pillow==10.0.0",
        "sqlalchemy==2.0.19",
        "pytz==2023.3",
        "python-dateutil==2.8.2"
    ]

    # 创建虚拟环境
    venv_path = "venv"
    if not os.path.exists(venv_path):
        print_colored("📁 创建虚拟环境...", Colors.BLUE)
        subprocess.run([sys.executable, "-m", "venv", venv_path], check=True)
        print_colored("✅ 虚拟环境创建成功", Colors.GREEN)

    # 根据操作系统确定pip路径
    if platform.system() == "Windows":
        pip_path = os.path.join(venv_path, "Scripts", "pip")
        python_path = os.path.join(venv_path, "Scripts", "python")
    else:
        pip_path = os.path.join(venv_path, "bin", "pip")
        python_path = os.path.join(venv_path, "bin", "python")

    # 升级pip
    print_colored("⬆️  升级pip...", Colors.BLUE)
    subprocess.run([pip_path, "install", "--upgrade", "pip"], capture_output=True)

    # 安装依赖
    total = len(dependencies)
    for i, dep in enumerate(dependencies, 1):
        print(f"   [{i}/{total}] 安装 {dep}...", end="")
        result = subprocess.run(
            [pip_path, "install", dep],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print_colored(" ✅", Colors.GREEN)
        else:
            print_colored(" ❌", Colors.FAIL)
            print_colored(f"      错误: {result.stderr}", Colors.WARNING)

    print_colored("✅ 依赖安装完成", Colors.GREEN)
    return python_path


class ConfigWizard:
    """配置向导"""

    def __init__(self):
        self.config = {
            'TELEGRAM_BOT_TOKEN': '',
            'HUOBI_API_KEY': '',
            'HUOBI_SECRET_KEY': '',
            'ALLOWED_USERS': '',
            'DEFAULT_SYMBOLS': 'btcusdt,ethusdt,bnbusdt',
            'GRID_LEVELS': '10',
            'GRID_PROFIT_RATE': '0.002',
            'LOG_LEVEL': 'INFO'
        }

    def run(self):
        """运行配置向导"""
        print_colored("\n⚙️  配置向导", Colors.HEADER)
        print_colored("-" * 50, Colors.CYAN)

        # Telegram配置
        self.configure_telegram()

        # 火币API配置
        self.configure_huobi()

        # 高级配置
        self.configure_advanced()

        # 保存配置
        self.save_config()

        return self.config

    def configure_telegram(self):
        """配置Telegram"""
        print_colored("\n📱 Telegram机器人配置", Colors.BLUE)
        print_colored("请按以下步骤获取Bot Token:", Colors.CYAN)
        print("1. 在Telegram中搜索 @BotFather")
        print("2. 发送 /newbot 创建新机器人")
        print("3. 设置机器人名称和用户名")
        print("4. 复制获得的Token")
        print()

        while True:
            token = input("请输入Bot Token: ").strip()
            if token and ":" in token:
                self.config['TELEGRAM_BOT_TOKEN'] = token
                print_colored("✅ Token已保存", Colors.GREEN)
                break
            else:
                print_colored("❌ Token格式不正确，请重新输入", Colors.FAIL)

        # 可选：限制用户
        print()
        user_ids = input("(可选) 限制使用的用户ID，多个用逗号分隔 [回车跳过]: ").strip()
        if user_ids:
            self.config['ALLOWED_USERS'] = user_ids
            print_colored("✅ 用户限制已设置", Colors.GREEN)

    def configure_huobi(self):
        """配置火币API"""
        print_colored("\n🔑 火币API配置", Colors.BLUE)
        print_colored("请按以下步骤获取API密钥:", Colors.CYAN)
        print("1. 登录火币官网 (www.huobi.com)")
        print("2. 进入 账户设置 -> API管理")
        print("3. 创建新的API密钥")
        print("4. 设置权限（建议只开启读取和交易）")
        print("5. 复制Access Key和Secret Key")
        print()

        # API Key
        while True:
            api_key = input("请输入API Access Key: ").strip()
            if api_key and len(api_key) > 20:
                self.config['HUOBI_API_KEY'] = api_key
                print_colored("✅ API Key已保存", Colors.GREEN)
                break
            else:
                print_colored("❌ API Key格式不正确", Colors.FAIL)

        # Secret Key
        while True:
            secret_key = input("请输入API Secret Key: ").strip()
            if secret_key and len(secret_key) > 20:
                self.config['HUOBI_SECRET_KEY'] = secret_key
                print_colored("✅ Secret Key已保存", Colors.GREEN)
                break
            else:
                print_colored("❌ Secret Key格式不正确", Colors.FAIL)

    def configure_advanced(self):
        """高级配置"""
        print_colored("\n⚙️  高级配置（可选）", Colors.BLUE)

        use_defaults = input("是否使用默认配置? [Y/n]: ").strip().lower()
        if use_defaults != 'n':
            print_colored("✅ 使用默认配置", Colors.GREEN)
            return

        # 交易对配置
        symbols = input(f"默认监控交易对 [{self.config['DEFAULT_SYMBOLS']}]: ").strip()
        if symbols:
            self.config['DEFAULT_SYMBOLS'] = symbols

        # 网格配置
        grid_levels = input(f"网格层数 [{self.config['GRID_LEVELS']}]: ").strip()
        if grid_levels and grid_levels.isdigit():
            self.config['GRID_LEVELS'] = grid_levels

        profit_rate = input(f"每格利润率 [{self.config['GRID_PROFIT_RATE']}]: ").strip()
        if profit_rate:
            try:
                float(profit_rate)
                self.config['GRID_PROFIT_RATE'] = profit_rate
            except:
                pass

        print_colored("✅ 高级配置完成", Colors.GREEN)

    def save_config(self):
        """保存配置到.env文件"""
        print_colored("\n💾 保存配置...", Colors.BLUE)

        env_content = f"""# Telegram Bot配置
TELEGRAM_BOT_TOKEN={self.config['TELEGRAM_BOT_TOKEN']}
ALLOWED_USERS={self.config['ALLOWED_USERS']}

# 火币API配置
HUOBI_API_KEY={self.config['HUOBI_API_KEY']}
HUOBI_SECRET_KEY={self.config['HUOBI_SECRET_KEY']}

# 交易配置
DEFAULT_SYMBOLS={self.config['DEFAULT_SYMBOLS']}
GRID_LEVELS={self.config['GRID_LEVELS']}
GRID_PROFIT_RATE={self.config['GRID_PROFIT_RATE']}

# 系统配置
LOG_LEVEL={self.config['LOG_LEVEL']}
LOG_FILE=logs/bot.log
DATABASE_URL=sqlite:///data/bot.db
"""

        with open('.env', 'w', encoding='utf-8') as f:
            f.write(env_content)

        print_colored("✅ 配置已保存到 .env 文件", Colors.GREEN)


class APITester:
    """API连接测试器"""

    def __init__(self, config):
        self.config = config
        self.base_url = "https://api.huobi.pro"

    def test_connection(self):
        """测试API连接"""
        print_colored("\n🔌 测试API连接...", Colors.HEADER)
        print_colored("-" * 50, Colors.CYAN)

        # 测试公共API
        if self.test_public_api():
            print_colored("✅ 公共API连接正常", Colors.GREEN)
        else:
            print_colored("❌ 公共API连接失败", Colors.FAIL)
            return False

        # 测试私有API
        if self.test_private_api():
            print_colored("✅ 私有API认证成功", Colors.GREEN)
            print_colored("✅ API密钥验证通过", Colors.GREEN)
            return True
        else:
            print_colored("❌ 私有API认证失败", Colors.FAIL)
            print_colored("   请检查API Key和Secret Key是否正确", Colors.WARNING)
            return False

    def test_public_api(self):
        """测试公共API"""
        print("   测试市场数据接口...")
        try:
            import requests
            response = requests.get(
                f"{self.base_url}/market/detail/merged",
                params={'symbol': 'btcusdt'},
                timeout=10
            )
            data = response.json()
            if data.get('status') == 'ok':
                price = data.get('tick', {}).get('close', 0)
                print(f"   BTC/USDT 当前价格: ${price:,.2f}")
                return True
        except Exception as e:
            print(f"   错误: {e}")
        return False

    def test_private_api(self):
        """测试私有API"""
        print("   测试账户接口...")
        try:
            import requests
            from datetime import datetime
            from urllib.parse import urlencode

            # 生成签名
            timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
            params = {
                'AccessKeyId': self.config['HUOBI_API_KEY'],
                'SignatureMethod': 'HmacSHA256',
                'SignatureVersion': '2',
                'Timestamp': timestamp,
            }

            # 构造签名字符串
            host = "api.huobi.pro"
            path = "/v1/account/accounts"
            sorted_params = sorted(params.items())
            encoded_params = urlencode(sorted_params)

            payload = f"GET\n{host}\n{path}\n{encoded_params}"

            # 计算签名
            signature = base64.b64encode(
                hmac.new(
                    self.config['HUOBI_SECRET_KEY'].encode('utf-8'),
                    payload.encode('utf-8'),
                    hashlib.sha256
                ).digest()
            ).decode('utf-8')

            params['Signature'] = signature

            # 发送请求
            response = requests.get(
                f"{self.base_url}{path}",
                params=params,
                timeout=10
            )

            data = response.json()
            if data.get('status') == 'ok':
                accounts = data.get('data', [])
                print(f"   找到 {len(accounts)} 个账户")
                for acc in accounts[:3]:
                    print(f"   - {acc['type']} 账户 (ID: {acc['id']})")
                return True
            else:
                print(f"   API错误: {data.get('err-msg', 'Unknown error')}")

        except Exception as e:
            print(f"   错误: {e}")
        return False


class ProjectGenerator:
    """项目文件生成器"""

    def __init__(self):
        self.project_name = "huobi_telegram_bot"

    def generate(self):
        """生成项目文件"""
        print_colored("\n📁 生成项目文件...", Colors.HEADER)
        print_colored("-" * 50, Colors.CYAN)

        # 创建目录结构
        self.create_directories()

        # 生成代码文件
        self.create_files()

        print_colored("✅ 项目文件生成完成", Colors.GREEN)

    def create_directories(self):
        """创建目录结构"""
        directories = [
            "api",
            "services",
            "strategies",
            "bot",
            "utils",
            "logs",
            "data"
        ]

        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            print(f"   📁 创建目录: {directory}")

    def create_files(self):
        """创建项目文件"""
        # 这里包含简化版的核心文件
        files = {
            "main.py": self.get_main_py(),
            "config.py": self.get_config_py(),
            "requirements.txt": self.get_requirements(),
            "api/__init__.py": "",
            "api/client.py": self.get_api_client(),
            "bot/__init__.py": "",
            "bot/handlers.py": self.get_bot_handlers(),
        }

        for filepath, content in files.items():
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"   📄 创建文件: {filepath}")

    def get_main_py(self):
        return '''"""火币交易Telegram机器人 - 主程序"""
import logging
import os
from datetime import datetime
from telegram.ext import Application, CommandHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    from config import Config
    from bot.handlers import BotHandlers

    config = Config()
    config.validate()

    app = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()

    handlers = BotHandlers()
    app.add_handler(CommandHandler("start", handlers.start))
    app.add_handler(CommandHandler("help", handlers.help))

    logger.info("机器人启动中...")
    app.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
'''

    def get_config_py(self):
        return '''"""配置管理"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    HUOBI_API_KEY = os.getenv('HUOBI_API_KEY')
    HUOBI_SECRET_KEY = os.getenv('HUOBI_SECRET_KEY')
    ALLOWED_USERS = os.getenv('ALLOWED_USERS', '').split(',') if os.getenv('ALLOWED_USERS') else []

    @classmethod
    def validate(cls):
        if not cls.TELEGRAM_BOT_TOKEN:
            raise ValueError("TELEGRAM_BOT_TOKEN is required")
        if not cls.HUOBI_API_KEY:
            raise ValueError("HUOBI_API_KEY is required")
        return True
'''

    def get_requirements(self):
        return '''python-telegram-bot==20.3
python-dotenv==1.0.0
requests==2.31.0
websocket-client==1.6.1
matplotlib==3.7.1
pandas==2.0.3
'''

    def get_api_client(self):
        return '''"""火币API客户端"""
import requests
import logging

logger = logging.getLogger(__name__)

class HuobiClient:
    def __init__(self, api_key, secret_key):
        self.api_key = api_key
        self.secret_key = secret_key
        self.base_url = "https://api.huobi.pro"

    def get_ticker(self, symbol):
        """获取行情"""
        try:
            response = requests.get(
                f"{self.base_url}/market/detail/merged",
                params={'symbol': symbol}
            )
            return response.json().get('tick', {})
        except Exception as e:
            logger.error(f"Get ticker failed: {e}")
            return {}
'''

    def get_bot_handlers(self):
        return '''"""Telegram消息处理器"""
from telegram import Update
from telegram.ext import ContextTypes
from config import Config
from api.client import HuobiClient

class BotHandlers:
    def __init__(self):
        self.config = Config()
        self.client = HuobiClient(
            self.config.HUOBI_API_KEY,
            self.config.HUOBI_SECRET_KEY
        )

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """处理/start命令"""
        await update.message.reply_text(
            "🤖 欢迎使用火币交易机器人！\\n"
            "使用 /help 查看帮助",
            parse_mode='MarkdownV2'
        )

    async def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """处理/help命令"""
        await update.message.reply_text("帮助信息：\\n/start - 启动机器人", parse_mode='MarkdownV2')
'''


def main():
    """主函数"""
    print_header()

    # 1. 环境检查
    print_colored("📋 环境检查", Colors.HEADER)
    print_colored("-" * 50, Colors.CYAN)

    if not check_python_version():
        print_colored("\n❌ 环境检查失败，请安装Python 3.8+", Colors.FAIL)
        input("\n按回车键退出...")
        return

    if not check_pip():
        print_colored("\n❌ pip未安装，请先安装pip", Colors.FAIL)
        input("\n按回车键退出...")
        return

    print_colored("✅ 环境检查通过\n", Colors.GREEN)

    # 2. 安装依赖
    choice = input("是否安装/更新依赖包? [Y/n]: ").strip().lower()
    if choice != 'n':
        python_path = install_dependencies()
    else:
        python_path = sys.executable

    # 3. 配置向导
    wizard = ConfigWizard()
    config = wizard.run()

    # 4. 测试API连接
    tester = APITester(config)
    if not tester.test_connection():
        print_colored("\n⚠️  API连接测试失败", Colors.WARNING)
        retry = input("是否重新配置API密钥? [Y/n]: ").strip().lower()
        if retry != 'n':
            wizard.configure_huobi()
            wizard.save_config()
            config = wizard.config
            if not tester.test_connection():
                print_colored("❌ API连接仍然失败，请检查配置", Colors.FAIL)
                input("\n按回车键退出...")
                return

    # 5. 生成项目文件
    generator = ProjectGenerator()
    generator.generate()

    # 6. 完成
    print_colored("\n" + "=" * 70, Colors.CYAN)
    print_colored("🎉 安装完成！", Colors.HEADER)
    print_colored("=" * 70, Colors.CYAN)

    print_colored("\n📝 后续步骤：", Colors.BLUE)
    print("1. 运行机器人:")
    if os.path.exists("venv"):
        if platform.system() == "Windows":
            print("   venv\\Scripts\\python main.py")
        else:
            print("   venv/bin/python main.py")
    else:
        print("   python main.py")

    print("\n2. 在Telegram中使用:")
    print("   - 搜索您的机器人")
    print("   - 发送 /start 开始使用")

    print_colored("\n💡 提示：", Colors.CYAN)
    print("- 日志文件位于: logs/bot.log")
    print("- 配置文件位于: .env")
    print("- 如需修改配置，编辑 .env 文件")

    # 询问是否立即启动
    print()
    start_now = input("是否立即启动机器人? [Y/n]: ").strip().lower()
    if start_now != 'n':
        print_colored("\n🚀 启动机器人...\n", Colors.GREEN)
        try:
            if os.path.exists("venv"):
                subprocess.run([python_path, "main.py"])
            else:
                subprocess.run([sys.executable, "main.py"])
        except KeyboardInterrupt:
            print_colored("\n\n👋 机器人已停止", Colors.CYAN)
        except Exception as e:
            print_colored(f"\n❌ 启动失败: {e}", Colors.FAIL)

    print_colored("\n感谢使用！祝您交易顺利！💰", Colors.GREEN)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_colored("\n\n❌ 安装已取消", Colors.WARNING)
    except Exception as e:
        print_colored(f"\n❌ 发生错误: {e}", Colors.FAIL)
        import traceback

        traceback.print_exc()
        input("\n按回车键退出...")