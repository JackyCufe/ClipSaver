#!/bin/bash
# ClipSaver: 把剪贴板截图保存到当前 Finder 窗口目录
# 用法：直接运行，或绑快捷键

# 获取当前 Finder 目录
FINDER_DIR=$(osascript -e '
tell application "Finder"
    if (count of windows) > 0 then
        POSIX path of (target of front window as alias)
    else
        POSIX path of (path to desktop)
    end if
' 2>/dev/null)

# 没有 Finder 窗口就存到桌面
TARGET_DIR="${FINDER_DIR:-$HOME/Desktop}"
FILENAME="screenshot-$(date +%Y%m%d-%H%M%S).png"
FILEPATH="$TARGET_DIR/$FILENAME"

# 保存
if pngpaste "$FILEPATH" 2>/dev/null; then
    # 在 Finder 中高亮显示
    open -R "$FILEPATH"
    # 系统通知
    osascript -e "display notification \"已保存: $FILENAME\" with title \"ClipSaver ✅\" subtitle \"$TARGET_DIR\""
else
    osascript -e "display notification \"剪贴板里没有图片\" with title \"ClipSaver ❌\""
fi
