@echo off
chcp 65001 >nul
title 自动控制原理题库 - 局域网设备共享服务器
echo ========================================================
echo   正在启动自动控制原理题库本地服务器...
echo ========================================================
echo.
python -c "
import socket
hostname = socket.gethostname()
ips = socket.gethostbyname_ex(hostname)[2]
lan_ips = [ip for ip in ips if not ip.startswith('127.')]
print('【电脑本机访问】:')
print('   http://localhost:8000')
print('')
print('【手机 / 平板 / 其他设备访问】(确保和电脑连接同一个 Wi-Fi 或手机热点):')
for ip in lan_ips:
    print(f'   http://{ip}:8000')
print('')
print('提示: 手机浏览器直接输入上述网址即可直接刷题！')
print('按 Ctrl + C 可关闭服务。')
"
echo.
echo ========================================================
python -m http.server 8000
pause
