# 贪吃蛇客户端游戏

基于 Python + Pygame 开发的桌面端贪吃蛇游戏，按 MVP、菜单、设置、存档、工程优化的节奏分阶段迭代。

## 当前进度

当前处于 `Sprint 9：输入服务抽象与可配置键位`。

已完成：

- MVP 玩法：蛇移动、食物、计分、游戏结束。
- 主菜单：开始游戏、继续游戏、设置、退出游戏。
- 设置系统：调整移动速度，并保存到 JSON。
- 键位设置：在设置页查看并修改游戏内移动、保存、暂停、重开按键。
- 多存档系统：开始游戏创建新存档槽，继续游戏显示多个存档，游戏中按 `E` 保存并返回主菜单。
- 中文 UI：菜单、设置、游戏提示、结束提示。
- 输入系统：Windows 环境下使用系统级 `GetAsyncKeyState` 兜底，并通过 `InputService` 统一管理动作键位。
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
- `E`：保存当前进度并返回主菜单。
- `P`：暂停或继续游戏。
- `Esc`：保存当前进度并返回主菜单。
- 游戏结束后按 `R`：重新开始。

设置页：

- `W/S` 或 `↑/↓`：切换选项。
- `A/D` 或 `←/→`：调整速度。
- `Enter` 或 `Space`：保存或确认。
- 选中某个键位后按 `Enter` 或 `Space`：进入改键状态。
- 改键状态下按一个新键：保存新键位并立即生效。
- 改键状态下按 `Esc`：取消改键。
- 鼠标点击返回按钮：返回主菜单。
- `Esc`：返回主菜单。

继续游戏页：

- 显示本地 `data/save.json` 中的多个存档。
- 每个存档显示序号、分数、蛇身长度和最后更新时间。
- `W/S` 或 `↑/↓`：切换存档按钮。
- `Enter` 或 `Space`：读取当前选中的存档。
- 鼠标悬停按钮时会同步高亮当前按钮。
- 鼠标左键点击存档按钮可以直接读取。

## 输入系统说明

本项目在 Windows 环境下不再依赖 Pygame 的字母键 `KEYDOWN` 作为唯一输入来源。

当前输入链路：

```text
config/key_bindings.json
  -> InputService
  -> system_keys.GetAsyncKeyState
  -> Scene.update()
  -> 菜单选择 / 游戏移动 / 保存 / 暂停
```

这样可以规避某些 Windows + 输入法 + Pygame/SDL 组合下，方向键正常但 `W/A/S/D` 无法进入 Pygame 事件队列的问题。

## 数据文件

- `config/settings.json`：保存移动速度设置。
- `config/settings.example.json`：仓库中的速度设置示例。
- `config/key_bindings.json`：保存动作到键位的映射，已加入 `.gitignore`，不会提交到 Git。
- `config/key_bindings.example.json`：仓库中的键位配置示例。
- `data/save.json`：本地真实运行存档，已加入 `.gitignore`，不会提交到 Git。
- `data/save.example.json`：仓库中的存档结构示例。

说明：

- 玩家关闭游戏后，本地 `data/save.json` 会保留。
- 玩家修改速度或键位后，本地 `config/settings.json` 和 `config/key_bindings.json` 会保留。
- 下一次启动游戏时，继续游戏页会继续读取本地 `data/save.json`。
- 后续开发提交代码时，不会再把玩家本地存档、速度设置、键位设置重置为空或默认值。

## 项目文档

- `docs/project_blueprint.md`：需求分析、架构设计和迭代计划。
- `docs/stage_progress.md`：阶段进度记录。
- `docs/incident_wasd_input_failure.md`：WASD 输入故障技术复盘报告。
- `docs/sprint_7_windows_input_final.md`：Sprint 7 输入系统最终说明。
- `docs/sprint_8_ui_components.md`：Sprint 8 UI 组件深化说明。
- `docs/sprint_8_multi_save_slots.md`：Sprint 8 多存档说明。
- `docs/sprint_9_input_service.md`：Sprint 9 输入服务说明。
- `docs/sprint_9_persistent_save_storage.md`：Sprint 9 本地存档持久化说明。
- `docs/sprint_9_key_binding_edit.md`：Sprint 9 键位修改与设置页优化说明。
