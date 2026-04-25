# Sprint 9：输入服务抽象第一小步

## 当前阶段

- 当前 Sprint：Sprint 9：输入服务抽象与可配置键位
- 本次任务：抽象统一输入服务，并引入 JSON 键位配置
- 下一阶段建议：Sprint 9 第二小步：设置页增加键位展示与重载入口

## 当前阶段目标

- 将散落在各个场景中的按键判断集中到 `InputService`。
- 新增 `config/key_bindings.json`，让键位映射从代码常量过渡到 JSON 配置。
- 保持当前所有操作行为不变，不在本阶段做按键录入 UI。

## 本阶段完成功能

- 新增 `InputService` 统一处理：
  - 按键是否刚刚按下。
  - 按键是否正在按住。
  - 场景切换时同步按键状态，避免按键穿透。
  - 游戏移动方向计算。
- 新增 `config/key_bindings.json`。
- 主菜单、设置页、继续游戏页、游戏页都改为通过 `InputService` 读取输入。
- 删除旧的 `src/core/input_keys.py`。
- 保持原有用户操作不变：
  - 主菜单 `W/S` 或方向键选择，`Enter/Space` 确认，`Esc` 退出。
  - 设置页 `A/D` 或左右方向键调速度。
  - 游戏页 `W/A/S/D` 或方向键移动，`E` 保存，`P` 暂停，`Esc` 返回菜单。
  - 继续游戏页 `W/S` 或方向键选择存档。

## 本阶段完成设计

### 输入服务层

- 新增文件：`src/core/input_service.py`
- 核心类：`InputService`
- 负责读取：
  - `config/key_bindings.json`
  - `system_keys.GetAsyncKeyState`
- 核心方法：
  - `just_pressed(action)`：KEYDOWN 风格的一次性触发。
  - `pressed(action)`：当前是否处于按下状态。
  - `sync(action)`：场景进入时同步当前按键状态。
  - `sync_many(actions)`：批量同步页面用到的动作。
  - `direction()`：返回游戏移动方向。

### 键位配置设计

- 新增文件：`config/key_bindings.json`
- 当前配置示例：

```json
{
  "move_up": ["UP", "W"],
  "move_down": ["DOWN", "S"],
  "move_left": ["LEFT", "A"],
  "move_right": ["RIGHT", "D"],
  "save_game": ["E"],
  "pause_game": ["P"]
}
```

- 如果配置缺失或非法，`InputService` 会回退到默认键位并重写配置文件。

### 页面与 UI 对应关系

#### 主菜单页面

- 页面：`MenuScene`
- UI：`MenuList`
- 输入动作：
  - `menu_up`：上移选项。
  - `menu_down`：下移选项。
  - `confirm`：执行当前选项。
  - `back`：退出游戏。

#### 设置页面

- 页面：`SettingsScene`
- UI：速度文本、返回主菜单文本。
- 输入动作：
  - `menu_up/menu_down`：切换选项。
  - `settings_left/settings_right`：调整速度。
  - `confirm`：保存设置或返回主菜单。
  - `back`：返回主菜单。

#### 继续游戏页面

- 页面：`ContinueScene`
- UI：多个存档按钮、返回主菜单按钮。
- 输入动作：
  - `menu_up/menu_down`：切换存档按钮。
  - `confirm`：读取当前存档或返回主菜单。
  - `back`：返回主菜单。

#### 游戏页面

- 页面：`GameplayScene`
- UI：蛇、食物、HUD、暂停遮罩。
- 输入动作：
  - `move_up/move_down/move_left/move_right`：控制蛇移动。
  - `save_game`：保存当前存档并返回主菜单。
  - `pause_game`：暂停或继续。
  - `restart_game`：游戏结束后重新开始。
  - `back`：保存并返回主菜单。

## 数据流设计

```text
config/key_bindings.json
  -> InputService._load_bindings()
  -> action -> key names
  -> key names -> Windows virtual keys
  -> system_keys.GetAsyncKeyState
  -> Scene.update()
  -> UI 选择 / 游戏移动 / 存档 / 暂停
```

## 涉及文件

- `config/key_bindings.json`
- `src/core/input_service.py`
- `src/core/input_keys.py`
- `src/app.py`
- `src/scenes/menu_scene.py`
- `src/scenes/settings_scene.py`
- `src/scenes/continue_scene.py`
- `src/scenes/gameplay_scene.py`
- `data/save.json`
- `docs/sprint_9_input_service.md`

## 验证情况

- 需要执行语法检查。
- 需要人工验证：
  - 主菜单键盘输入仍正常。
  - 设置页调速仍正常。
  - 继续游戏页存档选择仍正常。
  - 游戏页移动、保存、暂停、返回菜单仍正常。

## 下一阶段建议

- Sprint 9 第二小步：在设置页展示当前键位配置。
- 后续再做“修改键位”的 UI，不在本阶段一次性加入。
