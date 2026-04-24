# 贪吃蛇客户端游戏

基于 Python + Pygame 的桌面端贪吃蛇游戏，按阶段迭代开发。

## 当前进度

当前处于 `Sprint 7：工程优化第二小步`。

已完成：
- MVP 玩法：移动、食物、计分、游戏结束
- 主菜单：开始游戏、继续游戏、设置、退出游戏
- 设置系统：调整移动速度并保存到 JSON
- 存档系统：自动保存、继续游戏、无存档提示
- 中文 UI：菜单、设置、游戏提示、结束提示
- 工程优化：场景基类、文本组件、菜单组件、按钮组件、正式继续游戏页

## 环境要求

- Python 3.13+
- Pygame 2.6+

当前本机已验证解释器：

```powershell
D:\ananconda\python.exe
```

## 安装依赖

```powershell
cd D:\codex_project
& 'D:\ananconda\python.exe' -m pip install -r requirements.txt
```

## 启动游戏

```powershell
cd D:\codex_project
& 'D:\ananconda\python.exe' main.py
```

## 操作方式

主菜单：
- `W/S` 或 `↑/↓`：切换选项
- `Enter` 或空格：确认
- `ESC`：退出

游戏中：
- `W/A/S/D` 或方向键：控制移动方向
- `ESC`：返回主菜单并保存当前进度
- 游戏结束后按 `R`：重新开始

设置页：
- `W/S` 或 `↑/↓`：切换选项
- `A/D` 或 `←/→`：调整速度
- `Enter` 或空格：保存或确认
- `ESC`：返回主菜单

继续游戏页：
- 有存档时可继续游戏
- 无存档时显示提示并返回主菜单
- 支持键盘选择和鼠标点击按钮

## 数据文件

- `config/settings.json`：保存移动速度设置
- `data/save.json`：保存当前游戏进度

## 阶段记录

详细阶段进度见：

- `docs/stage_progress.md`
