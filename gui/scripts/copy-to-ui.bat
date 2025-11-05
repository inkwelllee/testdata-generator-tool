@echo off
echo 🚀 开始复制构建文件到ui目录...

set SOURCE_DIR=%~dp0..\dist
set TARGET_DIR=%~dp0..\..\asserts\ui

if not exist "%SOURCE_DIR%" (
    echo ❌ 构建目录不存在，请先运行 npm run build
    exit /b 1
)

echo 🧹 清空目标目录...
if exist "%TARGET_DIR%" (
    rmdir /s /q "%TARGET_DIR%"
)
mkdir "%TARGET_DIR%"

echo 📁 复制文件...
robocopy "%SOURCE_DIR%" "%TARGET_DIR%" /E /NFL /NDL /NJH /NJS

if %ERRORLEVEL% LEQ 1 (
    echo ✅ 文件复制完成！
    echo 📂 源目录: %SOURCE_DIR%
    echo 📂 目标目录: %TARGET_DIR%
) else (
    echo ❌ 复制过程中出现错误
    exit /b 1
)