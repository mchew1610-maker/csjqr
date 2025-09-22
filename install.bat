@echo off
echo ============================================================
echo         火币交易机器人 - 依赖安装脚本
echo ============================================================
echo.

echo [1/4] 升级 pip...
python -m pip install --upgrade pip

echo.
echo [2/4] 卸载旧版本 python-telegram-bot (如果存在)...
pip uninstall -y python-telegram-bot

echo.
echo [3/4] 安装 python-telegram-bot 带 job-queue 支持...
pip install "python-telegram-bot[job-queue]==20.3"

echo.
echo [4/4] 安装其他依赖...
pip install python-dotenv==1.0.0
pip install requests==2.31.0
pip install aiohttp==3.8.5
pip install websocket-client==1.6.1
pip install pandas==2.0.3
pip install numpy==1.24.3
pip install matplotlib==3.7.1
pip install pillow==10.0.0
pip install sqlalchemy==2.0.19
pip install pytz==2023.3
pip install python-dateutil==2.8.2
pip install APScheduler==3.10.1

echo.
echo ============================================================
echo         安装完成！
echo ============================================================
echo.
echo 现在可以运行: python main.py
echo.
pause