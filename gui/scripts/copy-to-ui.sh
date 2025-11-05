#!/bin/bash

echo "🚀 开始复制构建文件到ui目录..."

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_DIR="$SCRIPT_DIR/../dist"
TARGET_DIR="$SCRIPT_DIR/../../asserts/ui"

if [ ! -d "$SOURCE_DIR" ]; then
    echo "❌ 构建目录不存在，请先运行 npm run build"
    exit 1
fi

echo "🧹 清空目标目录..."
rm -rf "$TARGET_DIR"
mkdir -p "$TARGET_DIR"

echo "📁 复制文件..."
cp -r "$SOURCE_DIR"/* "$TARGET_DIR"/

if [ $? -eq 0 ]; then
    echo "✅ 文件复制完成！"
    echo "📂 源目录: $SOURCE_DIR"
    echo "📂 目标目录: $TARGET_DIR"
    
    # 统计文件数量
    FILE_COUNT=$(find "$TARGET_DIR" -type f | wc -l)
    echo "📊 共复制 $FILE_COUNT 个文件"
else
    echo "❌ 复制过程中出现错误"
    exit 1
fi