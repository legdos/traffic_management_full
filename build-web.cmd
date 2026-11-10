@echo off
REM 构建前端并把产物拷贝到后端 static 目录（单进程部署）
REM 用法：双击本文件，或在命令行执行 build-web.cmd
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0build-web.ps1"
pause
