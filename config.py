"""配置管理"""
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
