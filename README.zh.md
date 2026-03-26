[![English](https://img.shields.io/badge/README-English-blue)](README.md)

# ClipSaver 📋

**把剪贴板里的图片，一键存到当前 Finder 窗口目录。**

Mac 原生没有「剪贴板图片 → 直接存成文件」的路径，`⌘V` 在 Finder 里完全不管用。ClipSaver 补上这个缺口——不管图片怎么来的，系统截图、飞书截图、网页复制、Figma 导出，只要图片在剪贴板里，打开 Finder 切到目标目录，按 `⌘⌥V` 直接落地成 png 文件。同一张图想存几个地方，切目录再按一次就行。

---

## 使用方法

1. 截图，图片进入剪贴板
   - `⌘⌃⇧4` — 截图直接存入剪贴板（不落地文件，所有 macOS 版本均支持）
   - `⌘⇧4` — macOS Monterey (12)+ 截图同时自动复制到剪贴板
   - 或任意截图工具 / 复制网页图 / 从设计软件复制，只要图片在剪贴板里即可
2. 在 Finder 打开你想存的目录
3. 按 `⌘⌥V` — 图片以 `screenshot-HHMMSS.png` 保存到该目录，Finder 自动定位到文件
4. 想同时存到另一个目录？切过去再按一次

菜单栏出现 📋 图标说明正在运行。点图标可手动触发保存，或开启/关闭开机自启。

---

## 安装

**依赖**

```bash
pip install rumps pyobjc
brew install pngpaste
```

**运行**

```bash
python3 clipsaver.py
```

首次运行需要在「系统设置 → 隐私与安全性 → 辅助功能」中授权，用于监听全局快捷键。

**开机自启**

点菜单栏 📋 → 开机自启，无需额外配置。

---

## 系统要求

- macOS 12+
- Python 3.9+

---

## 实现原理

80 行 Python，三个核心依赖：

- **rumps** — 菜单栏 App 壳子
- **NSEvent (pyobjc)** — 系统级全局快捷键监听
- **pngpaste + osascript** — 剪贴板图片落地 & 获取 Finder 当前目录

---

## License

MIT
