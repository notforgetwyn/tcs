# 贪吃蛇客户端游戏

基于 Python + Pygame 开发的桌面端贪吃蛇游戏。项目按工程化方式分阶段推进：MVP、主菜单、设置、存档、工程优化。

## 当前进度

当前处于：`阶段 5：工程优化 / 优化 Sprint 14：README 操作说明补齐`

已完成能力：

- MVP 玩法：蛇移动、食物生成、吃食物加分、游戏结束判定。
- 主菜单：开始游戏、继续游戏、设置、退出游戏。
- 设置系统：调整移动速度，并保存到 JSON。
- 键位设置：可修改游戏移动、保存、暂停、重开等按键。
- 默认键位恢复：设置页支持一键恢复默认键位。
- 多存档系统：开始游戏创建新存档，继续游戏页显示多个存档。
- 存档管理：继续游戏页支持读取、重命名、删除存档。
- 游戏中保存：按保存键后保存当前进度并返回主菜单。
- 暂停功能：游戏中可以暂停和继续。
- 中文 UI：主菜单、设置页、继续游戏页、游戏提示、结束提示。
- Windows 系统级输入兜底：通过 `GetAsyncKeyState` 避免 Pygame 在部分环境收不到字母键事件。
- UI 组件化：已抽象 `Button`、`Panel`、`SaveCard`、`SettingRow`、`ScrollList`、`TextBlock` 等组件。

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

说明：

- 每次启动程序都会先进入主菜单。
- 游戏窗口运行期间，命令行看起来会一直占用，这是 Pygame 主循环的正常表现。
- 关闭窗口或在主菜单选择退出游戏即可结束程序。

## 操作方式

### 主菜单

- `W/S` 或 `↑/↓`：切换菜单选项。
- `Enter` 或 `Space`：确认当前选项。
- 鼠标左键点击按钮：直接执行对应操作。
- `Esc`：退出游戏。

主菜单按钮：

- `开始游戏`：创建一个新的存档槽并进入新游戏。
- `继续游戏`：进入继续游戏页，查看本地已有存档。
- `设置`：进入设置页。
- `退出游戏`：关闭程序。

### 游戏中

默认键位：

- `W/A/S/D` 或方向键：控制蛇移动方向。
- `E`：保存当前进度并返回主菜单。
- `P`：暂停或继续游戏。
- `Esc`：保存当前进度并返回主菜单。
- 游戏结束后按 `R`：重新开始一局新游戏。

规则说明：

- 吃到黄色方块后加分。
- 蛇撞到墙或撞到自己会游戏结束。
- 游戏中保存后会回到主菜单，之后可从继续游戏页读取该存档。

### 继续游戏页

- 页面会读取本地 `data/save.json` 中的所有存档。
- 每个存档卡片显示：序号、存档名、分数、蛇长度、最后更新时间。
- `W/S` 或 `↑/↓`：切换当前选中的存档或返回按钮。
- 鼠标滚轮：浏览更多存档。
- `Enter` 或 `Space`：读取当前选中的存档。
- 鼠标点击存档卡片主体：读取该存档。
- `N`：重命名当前选中的存档。
- 点击 `重命名`：重命名对应存档。
- `Delete`：删除当前选中的存档，需要二次确认。
- 点击 `删除`：删除对应存档，需要二次确认。
- `Esc`：返回主菜单；如果正在删除确认状态，则先取消删除。

重命名说明：

- 进入重命名状态后，输入新名称。
- `Enter`：保存新名称。
- `Backspace`：删除一个字符。
- `Esc`：取消重命名。
- 存档名不能为空，最长 24 个字符。

### 设置页

- `W/S` 或 `↑/↓`：切换设置项。
- 选中速度项时，`A/D` 或 `←/→`：调整蛇移动速度。
- 选中速度项后按 `Enter` 或 `Space`：保存速度设置。
- 选中某个键位项后按 `Enter` 或 `Space`：进入改键状态。
- 改键状态下按一个新键：保存新键位并立即生效。
- 改键状态下按 `Esc`：取消改键。
- 选中 `恢复默认键位` 后按 `Enter` 或点击按钮：恢复默认键位。
- 选中 `返回主菜单` 后按 `Enter` 或点击按钮：返回主菜单。
- `Esc`：返回主菜单；如果正在改键，则取消改键。

可修改键位：

- 上移
- 下移
- 左移
- 右移
- 保存并返回菜单
- 暂停/继续
- 游戏结束后重开

## 默认键位

默认键位来自 `config/key_bindings.example.json`：

| 动作 | 默认键位 |
| --- | --- |
| 菜单上移 | `UP / W` |
| 菜单下移 | `DOWN / S` |
| 设置左调 | `LEFT / A` |
| 设置右调 | `RIGHT / D` |
| 游戏上移 | `UP / W` |
| 游戏下移 | `DOWN / S` |
| 游戏左移 | `LEFT / A` |
| 游戏右移 | `RIGHT / D` |
| 保存游戏 | `E` |
| 暂停游戏 | `P` |
| 重新开始 | `R` |
| 删除存档 | `DELETE` |
| 重命名存档 | `N` |
| 调试输入显示 | `F3` |

## 输入系统说明

本项目在 Windows 环境下不再把 Pygame 的字母键 `KEYDOWN` 作为唯一输入来源。

当前输入链路：

```text
config/key_bindings.json
  -> InputService
  -> system_keys.GetAsyncKeyState
  -> Scene.update()
  -> 菜单选择 / 游戏移动 / 保存 / 暂停 / 设置
```

这样可以规避部分 Windows + 输入法 + Pygame/SDL 组合下，方向键正常但 `W/A/S/D` 无法进入 Pygame 事件队列的问题。

## 数据文件

运行时本地文件：

- `config/settings.json`：保存移动速度设置。
- `config/key_bindings.json`：保存动作到键位的映射。
- `data/save.json`：保存本地真实存档。

仓库示例文件：

- `config/settings.example.json`：速度配置示例。
- `config/key_bindings.example.json`：键位配置示例。
- `data/save.example.json`：存档结构示例。

持久化说明：

- `data/save.json` 是本地真实存档，关闭游戏后仍保留。
- `config/settings.json` 和 `config/key_bindings.json` 是本地玩家配置，关闭游戏后仍保留。
- 上述运行时文件已加入 `.gitignore`，不会被提交到 GitHub。
- 换一台机器克隆仓库后，会从 example/default 数据自动生成本地运行时 JSON。

## 项目结构

```text
D:\codex_project
├── main.py
├── requirements.txt
├── README.md
├── AGENTS.md
├── assets/
├── config/
│   ├── settings.example.json
│   └── key_bindings.example.json
├── data/
│   └── save.example.json
├── docs/
└── src/
    ├── app.py
    ├── constants.py
    ├── core/
    ├── models/
    ├── scenes/
    └── ui/
```

核心分层：

```text
┌─────────────────────────────────────────────────────┐
│                   UI 展示层                          │
│  Button / Panel / SaveCard / SettingRow / TextBlock  │
├─────────────────────────────────────────────────────┤
│                  应用控制层                           │
│  App / 场景切换 / 主循环 / Pygame 生命周期             │
├─────────────────────────────────────────────────────┤
│                  场景业务层                           │
│  MenuScene / GameplayScene / SettingsScene           │
│  ContinueScene                                       │
├─────────────────────────────────────────────────────┤
│                  领域模型层                           │
│  Snake / Food / GameState                            │
├─────────────────────────────────────────────────────┤
│                  输入服务层                           │
│  InputService / system_keys / key_bindings.json       │
├─────────────────────────────────────────────────────┤
│                  文件存储层                           │
│  SaveService / SettingsService / FileManager / JSON   │
└─────────────────────────────────────────────────────┘
```

## 项目文档

- `docs/project_blueprint.md`：需求分析、架构设计和迭代计划。
- `docs/stage_progress.md`：阶段进度记录。
- `docs/incident_wasd_input_failure.md`：WASD 输入故障技术复盘。
- `docs/sprint_7_windows_input_final.md`：Windows 系统级输入方案说明。
- `docs/sprint_8_ui_components.md`：UI 组件深化说明。
- `docs/sprint_8_save_flow_fix.md`：存档流程修复说明。
- `docs/sprint_8_multi_save_slots.md`：多存档说明。
- `docs/sprint_9_input_service.md`：输入服务说明。
- `docs/sprint_9_persistent_save_storage.md`：本地存档持久化说明。
- `docs/sprint_9_key_binding_edit.md`：键位修改与设置页优化说明。
- `docs/sprint_10_buttons_and_reset_keys.md`：存档操作按钮与键位恢复默认说明。
- `docs/sprint_11_button_unification.md`：按钮组件统一说明。
- `docs/sprint_12_ui_component_extraction.md`：UI 组件抽象说明。
- `docs/sprint_13_scroll_list.md`：滚动列表组件说明。
