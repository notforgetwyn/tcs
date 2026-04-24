# Sprint 7：Windows 系统级输入兜底最终说明

## 当前阶段

- 当前 Sprint：Sprint 7：工程优化第二小步
- 本次补充任务：修复 Pygame 环境下 `W/A/S/D` 字母键无法被游戏接收的问题
- 下一阶段建议：Sprint 8：UI 组件深化

## 本阶段完成目标

- 将键盘输入统一改为 Windows 系统级按键读取。
- 菜单、设置、继续游戏、游戏中页面不再依赖 Pygame 的 `KEYDOWN` 字母键事件。
- 菜单类页面使用系统按键状态做边沿检测，实现“按下一次触发一次”的 KEYDOWN 语义。
- 游戏移动使用系统按键当前状态，保证 `W/A/S/D` 和方向键转向及时。
- 鼠标点击逻辑保留 Pygame 鼠标事件，因为鼠标事件在当前环境中稳定可用。

## 本阶段完成页面与 UI 行为

### 主菜单页面

- 页面：`MenuScene`
- UI 组件：`MenuList`
- 可操作项：
  - `开始游戏`
  - `继续游戏`
  - `设置`
  - `退出游戏`
- 键盘行为：
  - `W` / `↑`：菜单选择上移一次
  - `S` / `↓`：菜单选择下移一次
  - `Enter` / `Space`：执行当前选中项
  - `Esc`：退出游戏
  - `F3`：打开或关闭输入调试显示
- 鼠标行为：
  - 左键点击菜单项：选中并执行该菜单项
- 业务结果：
  - `开始游戏` 进入新游戏
  - `继续游戏` 进入继续游戏页面
  - `设置` 进入设置页面
  - `退出游戏` 关闭程序

### 继续游戏页面

- 页面：`ContinueScene`
- UI 组件：`Button`
- 可操作项：
  - 有存档时显示 `继续游戏`
  - 始终显示 `返回主菜单`
- 键盘行为：
  - `W` / `↑`：按钮选择上移一次
  - `S` / `↓`：按钮选择下移一次
  - `Enter` / `Space`：执行当前按钮
  - `Esc`：返回主菜单
  - `F3`：打开或关闭输入调试显示
- 鼠标行为：
  - 左键点击按钮：执行对应操作
- 业务结果：
  - 有存档时可以恢复游戏状态
  - 无存档时只能返回主菜单

### 设置页面

- 页面：`SettingsScene`
- UI 组件：`MenuList` 风格选择项
- 可操作项：
  - `速度`
  - `返回主菜单`
- 键盘行为：
  - `W` / `↑`：选择上移一次
  - `S` / `↓`：选择下移一次
  - 选中 `速度` 时，`A` / `←`：降低速度档位
  - 选中 `速度` 时，`D` / `→`：提高速度档位
  - `Enter` / `Space`：保存设置或返回主菜单
  - `Esc`：返回主菜单
  - `F3`：打开或关闭输入调试显示
- 鼠标行为：
  - 左键点击 `返回主菜单`：返回主菜单
- 业务结果：
  - 速度设置保存到 JSON 配置
  - 新开游戏会读取最新速度设置

### 游戏页面

- 页面：`GameplayScene`
- UI 组件：
  - 网格
  - 蛇头与蛇身
  - 黄色食物
  - 分数 HUD
  - 游戏结束提示
- 键盘行为：
  - `W` / `↑`：向上转向
  - `S` / `↓`：向下转向
  - `A` / `←`：向左转向
  - `D` / `→`：向右转向
  - `Esc`：保存当前进度并返回主菜单
  - 游戏结束后 `R`：重新开始
  - `F3`：打开或关闭输入调试显示
- 鼠标行为：
  - 当前游戏页面无鼠标业务操作
- 业务结果：
  - 蛇按固定移动间隔前进
  - 吃到黄色食物加分并增长
  - 撞墙或撞到自己后游戏结束
  - 游戏中自动保存进度，游戏结束清除存档

## 本阶段输入数据流设计

```text
Windows 物理键盘
        │
        ▼
src/core/system_keys.py
        │
        ├─ GetAsyncKeyState 读取 Windows 虚拟键状态
        ├─ any_pressed 判断多个键是否有任意一个按下
        └─ KeyEdges 将持续按下转换为 KEYDOWN 风格的一次性触发
        │
        ▼
src/core/input_keys.py
        │
        ├─ pressed_up
        ├─ pressed_down
        ├─ pressed_left
        ├─ pressed_right
        └─ pressed_direction
        │
        ▼
各 Scene.update()
        │
        ├─ 菜单/设置/继续页：使用 KeyEdges.just_pressed 做一次性动作
        └─ 游戏页：使用 pressed_direction 做实时转向
        │
        ▼
业务对象
        │
        ├─ MenuList / Button 处理 UI 选择
        ├─ Snake.set_direction 处理蛇转向
        ├─ SaveService 处理存档
        └─ SettingsService 处理配置保存
```

## 本阶段核心设计变化

- 输入层从“Pygame 键盘事件驱动”调整为“Windows 系统级按键状态驱动”。
- 场景层不再直接判断 `pygame.K_w`、`pygame.K_s`、`pygame.K_a`、`pygame.K_d`。
- `system_keys.KeyEdges` 负责把系统按键状态转换成页面需要的 KEYDOWN 行为。
- `input_keys.py` 只负责方向语义，不再耦合 Pygame 事件对象。
- Pygame 事件循环继续负责窗口关闭和鼠标点击。

## 本阶段涉及文件

- `src/core/system_keys.py`
- `src/core/input_keys.py`
- `src/core/input_debug.py`
- `src/app.py`
- `src/scenes/menu_scene.py`
- `src/scenes/continue_scene.py`
- `src/scenes/settings_scene.py`
- `src/scenes/gameplay_scene.py`
- `tools/keyboard_probe.py`
- `tools/tk_keyboard_probe.py`
- `docs/incident_wasd_input_failure.md`
- `docs/sprint_7_windows_input_final.md`

## 验证情况

- 已执行语法检查：

```powershell
& 'D:\ananconda\python.exe' -m compileall main.py src tools
```

- 验证结果：通过。
- 说明：系统级输入依赖真实 Windows 键盘状态，最终交互效果需要在本机窗口中实际按键验证。

## 下一阶段建议

- 进入 Sprint 8：UI 组件深化。
- 抽象更正式的 `InputService`，为后续跨平台输入和可配置键位做准备。
- 完善按钮组件的 hover、按下、禁用状态。
- 更新 README，把 Windows 系统级输入兜底写入启动与排障说明。
