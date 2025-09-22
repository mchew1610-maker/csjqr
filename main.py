"""
火币交易Telegram机器人 - 主程序（保留所有功能，只修复路径）
"""
import logging
import sys
import os
from datetime import datetime
from pathlib import Path

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    ContextTypes
)

# 修复路径问题 - 确保在正确的目录
BASE_DIR = Path(__file__).resolve().parent
os.chdir(BASE_DIR)  # 切换到 main.py 所在目录
sys.path.insert(0, str(BASE_DIR))

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
        """初始化机器人"""
        self.config = Config()
        self.handlers = None
        self.app = None

    def setup_handlers(self):
        """设置消息处理器"""
        # 创建处理器实例
        self.handlers = BotHandlers()

        # 重要：调用 setup 方法初始化定时任务
        self.handlers.setup(self.app)
        logger.info("定时任务已设置")

        # 命令处理器
        self.app.add_handler(CommandHandler("start", self.handlers.start))
        self.app.add_handler(CommandHandler("help", self.handlers.help))

        # 快捷命令处理器
        self.app.add_handler(CommandHandler("balance", self.balance_command))
        self.app.add_handler(CommandHandler("price", self.price_command))
        self.app.add_handler(CommandHandler("watch", self.watch_command))
        self.app.add_handler(CommandHandler("alert", self.alert_command))

        # 回调查询处理器（处理内联按钮点击）
        self.app.add_handler(CallbackQueryHandler(self.handlers.handle_callback_query))

        # 文本消息处理器（处理非命令文本）
        self.app.add_handler(MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            self.handlers.handle_text_message
        ))

        logger.info("所有处理器已注册")

    async def balance_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """处理 /balance 命令"""
        try:
            total = self.handlers.calculate_total_balance()
            await update.message.reply_text(f"💰 总资产: ${total:,.2f}")
        except Exception as e:
            logger.error(f"获取余额失败: {e}")
            await update.message.reply_text("❌ 获取余额失败，请稍后重试")

    async def price_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """处理 /price 命令"""
        if context.args:
            coin = context.args[0].lower()
            await self.handlers.handle_price_command(update, coin)
        else:
            await update.message.reply_text(
                "📌 使用方法: /price <币种>\n"
                "示例: /price btc"
            )

    async def watch_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """处理 /watch 命令"""
        user_id = str(update.effective_user.id)
        if context.args:
            coin = context.args[0].lower()
            await self.handlers.handle_watch_command(update, user_id, coin)
        else:
            await update.message.reply_text(
                "📌 使用方法: /watch <币种>\n"
                "示例: /watch btc"
            )

    async def alert_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """处理 /alert 命令"""
        user_id = str(update.effective_user.id)
        if len(context.args) >= 2:
            # 重建命令文本
            text = f"/alert {' '.join(context.args)}"
            await self.handlers.handle_alert_command(update, user_id, text)
        else:
            await update.message.reply_text(
                "📌 使用方法: /alert <币种> <价格>\n"
                "示例: /alert btc 100000\n"
                "当价格突破或跌破设定值时提醒"
            )

    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """全局错误处理器"""
        logger.error(f"Update {update} caused error: {context.error}")

        # 尝试通知用户
        if update and update.effective_message:
            try:
                error_message = "❌ 发生错误，请稍后重试"

                # 针对特定错误提供更详细的信息
                if "Forbidden" in str(context.error):
                    error_message = "❌ 机器人被封禁或没有权限"
                elif "NetworkError" in str(context.error):
                    error_message = "❌ 网络错误，请检查连接"
                elif "TimedOut" in str(context.error):
                    error_message = "❌ 请求超时，请稍后重试"

                await update.effective_message.reply_text(error_message)
            except Exception as e:
                logger.error(f"Failed to send error message: {e}")

    async def post_init(self, application: Application) -> None:
        """应用初始化后的回调"""
        logger.info("机器人初始化完成")
        # 可以在这里添加启动时的初始化任务

    async def shutdown(self, application: Application) -> None:
        """应用关闭前的回调"""
        logger.info("机器人正在关闭...")
        # 保存数据
        if self.handlers:
            self.handlers.save_user_data('watchlist', self.handlers.user_watchlist)
            self.handlers.save_user_data('alerts', self.handlers.price_alerts)
            self.handlers.save_user_data('balance_history', self.handlers.balance_history)
            logger.info("用户数据已保存")

    def run(self):
        """运行机器人"""
        try:
            # 验证配置
            self.config.validate()
            logger.info("配置验证通过")

            # 创建应用
            builder = Application.builder()
            builder.token(self.config.TELEGRAM_BOT_TOKEN)

            # 设置初始化和关闭回调
            builder.post_init(self.post_init)
            builder.post_shutdown(self.shutdown)

            # 构建应用
            self.app = builder.build()

            # 设置处理器
            self.setup_handlers()

            # 添加错误处理器
            self.app.add_error_handler(self.error_handler)

            # 打印启动信息
            print("=" * 60)
            print("         🤖 火币交易 Telegram 机器人")
            print("=" * 60)
            print(f"📅 启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("✅ 机器人已启动，正在监听消息...")
            print("=" * 60)
            print("按 Ctrl+C 停止机器人")
            print("")

            logger.info("开始轮询消息...")

            # 运行机器人
            self.app.run_polling(
                allowed_updates=Update.ALL_TYPES,
                drop_pending_updates=True,
                poll_interval=1,
                timeout=30
            )

        except KeyboardInterrupt:
            logger.info("收到中断信号，正在停止机器人...")
            print("\n👋 机器人已停止")
        except Exception as e:
            logger.error(f"机器人运行失败: {e}")
            print(f"\n❌ 机器人运行失败: {e}")
            raise

def check_environment():
    """检查运行环境"""
    # 检查Python版本
    if sys.version_info < (3, 8):
        print(f"❌ Python版本过低: {sys.version}")
        print("需要 Python 3.8 或更高版本")
        return False

    # 检查必要的包
    required_packages = [
        'telegram',
        'dotenv',
        'requests'
    ]

    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)

    if missing_packages:
        print(f"❌ 缺少必要的包: {', '.join(missing_packages)}")
        print("请运行: pip install -r requirements.txt")
        return False

    return True

def create_directories():
    """创建必要的目录"""
    directories = ['logs', 'data']
    for directory in directories:
        dir_path = BASE_DIR / directory
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
            logger.info(f"创建目录: {directory}")

def main():
    """主函数"""
    try:
        # ASCII艺术标题
        print("""
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║     🤖 火币交易 Telegram 机器人 v3.0                    ║
║                                                          ║
║     功能特性：                                           ║
║     • 实时行情监控                                      ║
║     • 技术分析 (金叉/死叉)                             ║
║     • 智能交易建议                                      ║
║     • 价格异动提醒                                      ║
║     • 自选币种管理                                      ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
        """)

        # 检查环境
        if not check_environment():
            print("\n❌ 环境检查失败，请修复问题后重试")
            sys.exit(1)

        print("✅ 环境检查通过")

        # 创建必要目录
        create_directories()

        # 检查配置文件（现在会在正确的目录查找）
        env_file = BASE_DIR / '.env'
        if not env_file.exists():
            print("\n⚠️  未找到 .env 配置文件")
            print(f"当前查找路径: {env_file}")

            # 检查是否有 .env.example
            env_example = BASE_DIR / '.env.example'
            if env_example.exists():
                print("请复制 .env.example 为 .env 并填入您的配置")
                print(f"命令: copy {env_example} {env_file}")
            else:
                print("请创建 .env 文件并填入配置")

            sys.exit(1)

        print(f"✅ 配置文件已找到: {env_file}")
        print("\n正在启动机器人...\n")

        # 运行机器人
        bot = HuobiTradingBot()
        bot.run()

    except KeyboardInterrupt:
        print("\n\n👋 再见！")
        sys.exit(0)
    except Exception as e:
        logger.error(f"程序异常: {e}", exc_info=True)
        print(f"\n❌ 程序异常: {e}")
        print("\n请检查日志文件: logs/bot.log")
        sys.exit(1)

if __name__ == '__main__':
    main()