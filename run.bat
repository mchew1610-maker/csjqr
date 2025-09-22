@echo off
echo ============================================================
echo         火币交易机器人 - 修复安装脚本
echo ============================================================
echo.

echo [步骤 1/5] 卸载有问题的版本...
pip uninstall -y python-telegram-bot
pip uninstall -y APScheduler

echo.
echo [步骤 2/5] 清理pip缓存...
pip cache purge

echo.
echo [步骤 3/5] 安装稳定版本的python-telegram-bot...
pip install python-telegram-bot==20.2

echo.
echo [步骤 4/5] 安装其他依赖...
pip install python-dotenv==1.0.0
pip install requests==2.31.0
pip install websocket-client==1.6.1
pip install pytz==2023.3
pip install python-dateutil==2.8.2

echo.
echo [步骤 5/5] 验证安装...
python -c "import telegram; print(f'Telegram Bot版本: {telegram.__version__}')"

echo.
echo ============================================================
echo         ✅ 修复完成！
echo ============================================================
echo.
echo 现在可以运行: python main.py
echo.
pause