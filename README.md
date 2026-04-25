# 贪吃蛇客户端游戏

基于 Python + Pygame 开发的桌面端贪吃蛇游戏，按 MVP、菜单、设置、存档、工程优化的节奏分阶段迭代。

## 当前进度

当前处于 `Sprint 8：UI 组件深化`。

已完成：

- MVP 玩法：蛇移动、食物、计分、游戏结束。
- 主菜单：开始游戏、继续游戏、设置、退出游戏。
- 设置系统：调整移动速度，并保存到 JSON。
- 存档系统：自动保存、继续游戏、无存档提示。
- 中文 UI：菜单、设置、游戏提示、结束提示。
- 输入修复：Windows 环境下使用系统级 `GetAsyncKeyState` 兜底，解决 Pygame 收不到 `W/A/S/D` 的问题。
- UI 组件：文本组件、菜单组件、按钮组件、继续游戏页面按钮 hover/selected 状态。

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

- `W/S` 或 `↑/↓`：切换选项。
- `Enter` 或 `Space`：确认。
- 鼠标左键点击菜单项：直接执行对应操作。
- `Esc`：退出游戏。

游戏中：

- `W/A/S/D` 或方向键：控制移动方向。
- `Esc`：保存当前进度并返回主菜单。
- 游戏结束后按 `R`：重新开始。

设置页：

- `W/S` 或 `↑/↓`：切换选项。
- `A/D` 或 `←/→`：调整速度。
- `Enter` 或 `Space`：保存或确认。
- 鼠标点击返回按钮：返回主菜单。
- `Esc`：返回主菜单。

继续游戏页：

- 有存档时可以继续游戏。
- 无存档时显示提示，并提供返回主菜单按钮。
- 支持键盘选择和鼠标点击按钮。
- 鼠标悬停按钮时会同步高亮当前按钮。

## 输入系统说明

本项目在 Windows 环境下不再依赖 Pygame 的字母键 `KEYDOWN` 作为唯一输入来源。

当前输入链路：

```text
Windows 物理键盘
  -> src/core/system_keys.py
  -> GetAsyncKeyState
  -> KeyEdges / input_keys
  -> Scene.update()
  -> 菜单选择 / 游戏移动 / 设置调整
```

这样可以规避某些 Windows + 输入法 + Pygame/SDL 组合下，方向键正常但 `W/A/S/D` 无法进入 Pygame 事件队列的问题。

## 数据文件

- `config/settings.json`：保存移动速度设置。
- `config/key_bindings.json`：保存动作到键位的映射。
- `data/save.json`：保存当前游戏进度。

## 项目文档

- `docs/project_blueprint.md`：需求分析、架构设计和迭代计划。
- `docs/stage_progress.md`：阶段进度记录。
- `docs/incident_wasd_input_failure.md`：WASD 输入故障技术复盘报告。
- `docs/sprint_7_windows_input_final.md`：Sprint 7 输入系统最终说明。
- `docs/sprint_8_ui_components.md`：Sprint 8 UI 组件深化说明。
