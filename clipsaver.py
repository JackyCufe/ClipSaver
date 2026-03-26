#!/usr/bin/env python3
"""
ClipSaver - 全局快捷键截图粘贴工具
⌘⌥V 自动把剪贴板截图存到当前 Finder 窗口目录
"""
import rumps
import subprocess
import os
import datetime
import threading

from Cocoa import NSEvent, NSKeyDownMask

# ── 核心：保存截图 ─────────────────────────────────────────────────────────────
def get_finder_dir():
    r = subprocess.run(['osascript', '-e', '''
        tell application "Finder"
            if (count of windows) > 0 then
                POSIX path of (target of front window as alias)
            else
                POSIX path of (path to desktop)
            end if
        end tell
    '''], capture_output=True, text=True, timeout=3)
    return r.stdout.strip() or os.path.expanduser('~/Desktop')

def do_paste():
    target = get_finder_dir()
    name = f'screenshot-{datetime.datetime.now().strftime("%H%M%S")}.png'
    path = os.path.join(target, name)
    r = subprocess.run(['pngpaste', path], capture_output=True)
    if r.returncode == 0:
        subprocess.run(['open', '-R', path])
        rumps.notification('ClipSaver', '已保存', f'{name}\n→ {os.path.basename(target)}')
    else:
        rumps.notification('ClipSaver', '❌ 剪贴板无图片', '请先截图再按 ⌘⌥V')

# ── menubar app ────────────────────────────────────────────────────────────────
class App(rumps.App):
    def __init__(self):
        super().__init__('📋', quit_button=None)
        self.menu = [
            rumps.MenuItem('保存截图  ⌘⌥V', callback=lambda _: threading.Thread(target=do_paste).start()),
            None,
            rumps.MenuItem('开机自启', callback=self.toggle_login),
            None,
            rumps.MenuItem('退出 ClipSaver', callback=rumps.quit_application),
        ]
        # 注册全局快捷键 ⌘⌥V
        # keyCode 9 = V
        # NSCommandKeyMask  = 1 << 20 = 0x100000
        # NSAlternateKeyMask = 1 << 19 = 0x080000
        NSEvent.addGlobalMonitorForEventsMatchingMask_handler_(
            NSKeyDownMask,
            self._on_key
        )

    def _on_key(self, event):
        if event.keyCode() == 9:  # V
            flags = event.modifierFlags()
            cmd = bool(flags & 0x100000)  # ⌘
            opt = bool(flags & 0x080000)  # ⌥
            sft = bool(flags & 0x020000)  # ⇧（确保没按 Shift）
            if cmd and opt and not sft:
                threading.Thread(target=do_paste).start()

    def toggle_login(self, sender):
        plist = os.path.expanduser('~/Library/LaunchAgents/com.clipsaver.plist')
        if os.path.exists(plist):
            subprocess.run(['launchctl', 'unload', plist])
            os.remove(plist)
            sender.title = '开机自启'
            rumps.notification('ClipSaver', '已关闭开机自启', '')
        else:
            script_path = os.path.abspath(__file__)
            python_path = subprocess.run(['which', 'python3'], capture_output=True, text=True).stdout.strip()
            content = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
  <key>Label</key><string>com.clipsaver</string>
  <key>ProgramArguments</key>
  <array><string>{python_path}</string><string>{script_path}</string></array>
  <key>RunAtLoad</key><true/>
  <key>KeepAlive</key><true/>
</dict></plist>'''
            with open(plist, 'w') as f: f.write(content)
            subprocess.run(['launchctl', 'load', plist])
            sender.title = '✅ 开机自启（已开启）'
            rumps.notification('ClipSaver', '已开启开机自启', '')

if __name__ == '__main__':
    App().run()
