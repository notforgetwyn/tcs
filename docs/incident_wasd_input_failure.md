# 技术错误报告：Pygame 环境下 W/A/S/D 输入失效

## 1. 报告信息

- 项目名称：Python + Pygame 贪吃蛇客户端
- 报告类型：客户端输入系统故障复盘
- 当前 Sprint：Sprint 7 工程优化第二小步
- 问题状态：已解决
- 影响模块：
  - `src/core/input_keys.py`
  - `src/core/system_keys.py`
  - `src/scenes/menu_scene.py`
  - `src/scenes/settings_scene.py`
  - `src/scenes/gameplay_scene.py`
  - `src/scenes/continue_scene.py`

## 2. 问题摘要

在 Windows 环境下运行 Pygame 贪吃蛇客户端时，方向键可以正常控制菜单和蛇移动，但 `W/A/S/D` 字母键无法生效。

该问题最初被误判为业务输入逻辑缺陷，后续通过 Pygame 调试窗口和 Tkinter 对照测试确认：Windows 系统和键盘本身可以正常接收字母键，但 Pygame/SDL 在当前运行环境下没有向游戏窗口上报 `W/A/S/D` 的字母键事件。

最终通过增加 Windows 系统级按键读取兜底 `GetAsyncKeyState` 解决。

## 3. 用户可见影响

### 3.1 受影响功能

- 主菜单中 `W/S` 无法切换选项。
- 设置页中 `W/S/A/D` 无法切换选项或调整速度。
- 游戏页中 `W/A/S/D` 无法控制蛇移动。

### 3.2 未受影响功能

- 方向键正常。
- `Enter`、`ESC` 等控制键正常。
- 鼠标点击在补充修复后正常。
- 游戏核心逻辑正常，包括移动、食物、计分、存档、读档。

## 4. 时间线

### 阶段 1：用户反馈

用户反馈：
- 方向键可用。
- `W/A/S/D` 不可用。
- 按 `W/A/S/D` 后，再按方向键也出现异常体验。

初步判断：
- 事件循环可能没有正确处理字母键。
- 菜单输入逻辑和游戏输入逻辑可能存在设计问题。

### 阶段 2：第一次修复尝试

处理方式：
- 将菜单和游戏输入从单一 `KEYDOWN` 调整为轮询 `pygame.key.get_pressed()`。

结果：
- 未解决问题。
- 轮询还引入了菜单响应节奏不清晰的问题。

复盘结论：
- 菜单这类“按一下移动一次”的交互不适合只依赖轮询。
- 应优先使用 `KEYDOWN`，轮询只能作为补充。

### 阶段 3：第二次修复尝试

处理方式：
- 将输入逻辑恢复为纯 `KEYDOWN`。
- 增加对 `pygame.K_w/K_a/K_s/K_d` 物理按键码的判断。
- 增加对 `event.scancode` 的判断。

结果：
- 方向键仍正常。
- `W/A/S/D` 仍不可用。

复盘结论：
- 问题不只是 `event.unicode` 为空。
- Pygame 可能没有收到字母键事件。

### 阶段 4：Pygame 调试验证

处理方式：
- 增加 `F3` 输入调试显示。
- 在窗口底部显示最新按键事件：
  - `event.key`
  - `event.scancode`
  - `event.unicode`

验证结果：
- 方向键按下后，调试信息正常变化。
- `W/A/S/D` 按下后，调试信息完全不变。

复盘结论：
- Pygame 的事件队列没有收到 `W/A/S/D` 的 `KEYDOWN`。
- 问题不是业务层 `Snake.set_direction()` 或菜单选择逻辑。

### 阶段 5：TEXTINPUT 兜底尝试

处理方式：
- 启用 `pygame.key.start_text_input()`。
- 增加对 `pygame.TEXTINPUT` 的处理。

结果：
- 无窗口模拟测试通过。
- 实际用户环境中仍然无法解决。

复盘结论：
- 当前环境下 Pygame/SDL 既没有收到字母键 `KEYDOWN`，也没有稳定收到 `TEXTINPUT`。

### 阶段 6：独立 Tkinter 对照测试

处理方式：
- 创建完全不依赖 Pygame 的 Tkinter 测试程序：
  - `tools/tk_keyboard_probe.py`

用户反馈 Tkinter 能收到字母键：

```text
KeyPress keysym='D' keycode=68 char='D' state=10
KeyPress keysym='W' keycode=87 char='W' state=10
```

复盘结论：
- 键盘硬件正常。
- Windows 系统输入正常。
- Tkinter 可以收到字母键。
- 故障范围收敛到 Pygame/SDL 输入层。

### 阶段 7：最终修复

处理方式：
- 新增 Windows 系统级输入兜底模块：
  - `src/core/system_keys.py`
- 使用 Windows API：
  - `GetAsyncKeyState`
- 在 `src/core/input_keys.py` 中接入系统级兜底。

最终输入链路：

```text
Pygame KEYDOWN
  ↓
Pygame TEXTINPUT
  ↓
Pygame key.get_pressed()
  ↓
Windows GetAsyncKeyState
```

结果：
- 用户确认 `W/A/S/D` 可以使用。

## 5. 根因分析

### 5.1 直接原因

Pygame/SDL 在当前 Windows 输入环境下没有向游戏窗口上报 `W/A/S/D` 字母键事件。

表现为：

```text
方向键能触发 Pygame 事件
W/A/S/D 不能触发 Pygame 事件
Tkinter 能收到 W/A/S/D
```

### 5.2 深层原因

当前环境中可能存在以下因素之一：

- 中文输入法或输入法状态影响 SDL 字母键事件上报。
- SDL 与当前键盘布局兼容异常。
- Pygame 窗口可收到非文本控制键，但字母键被系统文本输入层或输入法层处理。
- Pygame/SDL 在该 Python/Windows/输入法组合下存在字母键事件上报异常。

### 5.3 为什么方向键正常

方向键属于非文本控制键，不依赖输入法文本输入链路。

因此方向键可以通过 `KEYDOWN` 正常进入 Pygame，而 `W/A/S/D` 属于文本类按键，可能被输入法或 SDL 文本输入层影响。

## 6. 解决方案

### 6.1 新增系统级输入模块

新增文件：

- `src/core/system_keys.py`

核心能力：

```python
GetAsyncKeyState
```

作用：

- 直接向 Windows 查询当前物理按键是否按下。
- 不依赖 Pygame。
- 不依赖 SDL。
- 不依赖输入法文本事件。

### 6.2 输入识别统一入口

更新文件：

- `src/core/input_keys.py`

输入识别优先级：

```text
1. Pygame event.key
2. Pygame event.scancode
3. Pygame event.unicode
4. Pygame key.get_pressed()
5. Windows GetAsyncKeyState
```

### 6.3 场景接入

接入页面：

- `MenuScene`
- `SettingsScene`
- `GameplayScene`
- `ContinueScene`

接入结果：

- 主菜单可用 `W/S` 切换。
- 设置页可用 `W/S/A/D` 操作。
- 游戏页可用 `W/A/S/D` 控制蛇移动。
- 继续游戏页可用 `W/S` 切换按钮。

## 7. 验证结果

### 7.1 自动验证

已执行：

```powershell
& 'D:\ananconda\python.exe' -m compileall main.py src
```

结果：

- 语法检查通过。

### 7.2 对照验证

Pygame 调试：

- 方向键有事件。
- 字母键无事件。

Tkinter 调试：

- `W/D` 有事件。

结论：

- 系统输入正常。
- Pygame/SDL 输入层异常。

### 7.3 用户验证

用户反馈：

```text
ok 可以了
```

结论：

- Windows 系统级输入兜底方案生效。

## 8. 代码变更清单

新增文件：

- `src/core/system_keys.py`
- `src/core/input_debug.py`
- `tools/keyboard_probe.py`
- `tools/tk_keyboard_probe.py`

修改文件：

- `src/core/input_keys.py`
- `src/app.py`
- `src/scenes/menu_scene.py`
- `src/scenes/settings_scene.py`
- `src/scenes/gameplay_scene.py`
- `src/scenes/continue_scene.py`

## 9. 经验教训

### 9.1 输入系统不能只依赖单一通道

桌面游戏输入尤其在 Windows + 输入法环境下，不能默认 Pygame/SDL 一定能收到所有键盘事件。

对于关键输入，应具备多层兜底：

```text
事件输入
状态输入
系统级输入
```

### 9.2 方向键正常不代表字母键正常

方向键和字母键在系统输入链路中不是完全一样的类型。

方向键属于控制键，字母键可能受到输入法、键盘布局、文本输入层影响。

### 9.3 排查需要独立对照程序

本次关键证据来自 Tkinter 测试。

如果只在贪吃蛇内部反复修改，很容易误判为业务代码问题。

### 9.4 调试工具应该保留为开发能力

`F3` 输入调试显示可以在开发期保留，但后续正式版本应考虑：

- 默认关闭。
- 仅开发模式启用。
- 或迁移到日志/诊断模块。

## 10. 后续行动

### 10.1 短期行动

- 将 Windows 输入兜底纳入输入系统正式设计。
- 将 `F3` 输入调试能力标记为开发工具。
- 更新 README，说明 Windows 环境下已加入系统级输入兜底。
- 提交并推送本次修复。

### 10.2 中期行动

- 增加可配置键位。
- 将按键映射写入 JSON 配置。
- 设置页增加键位配置入口。

### 10.3 长期行动

- 抽象跨平台输入层：

```text
InputService
  ↓
PygameInputProvider
WindowsInputProvider
ConfigurableKeyMap
```

- Windows 使用 `GetAsyncKeyState` 兜底。
- 非 Windows 平台保留 Pygame 标准输入。
- 后续支持手柄或其他输入设备时，统一接入 `InputService`。
