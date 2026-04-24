# Sprint 7 补充更新：输入与鼠标交互修复

当前 Sprint：
- `Sprint 7：工程优化第二小步`

本次补充修复功能：
- 修复 `W/A/S/D` 在中文输入法或特殊键盘布局下无响应的问题。
- 主菜单支持鼠标点击菜单项。
- 设置页支持鼠标点击 `返回主菜单`。
- 继续游戏页沿用 `Button` 鼠标点击能力。

本次补充完成设计：
- 新增 `src/core/input_keys.py`，集中管理输入识别。
- 输入识别顺序调整为：方向键/字母物理按键码 -> SDL `scancode` -> `event.unicode`。
- `MenuScene`、`SettingsScene`、`GameplayScene`、`ContinueScene` 统一使用 `input_keys` 判断 `W/A/S/D` 和方向键。
- `MenuList` 新增 `hit_test()`，用于主菜单和设置页的鼠标命中检测。

页面与 UI 交互补充：
- 主菜单 `MenuScene`：点击 `开始游戏`、`继续游戏`、`设置`、`退出游戏` 文本区域后，会直接执行对应操作。
- 设置页 `SettingsScene`：点击 `返回主菜单` 文本区域后，会返回主菜单；点击速度区域只选中速度项，速度仍通过键盘调整。
- 游戏页 `GameplayScene`：`W/A/S/D` 现在不依赖 `event.unicode`，即使 `unicode` 为空，只要 SDL 扫描码是对应物理键，也能转向。
- 继续游戏页 `ContinueScene`：`W/S` 也接入统一输入工具，鼠标点击按钮继续保持可用。

数据流补充：
- 键盘输入数据流：`KEYDOWN` -> `input_keys` 检查 `event.key` / `event.scancode` / `event.unicode` -> 场景执行菜单移动、设置调整或游戏转向。
- 鼠标点击数据流：`MOUSEBUTTONDOWN` -> `MenuList.hit_test()` 或 `Button.contains()` -> 更新选中项 -> 执行业务动作。

验证情况：
- 已通过语法检查。
- 已用无窗口测试验证 `event.key=0`、`event.unicode=""`、仅有 `scancode` 时，主菜单 `W/S` 可用。
- 已用无窗口测试验证 `event.key=0`、`event.unicode=""`、仅有 `scancode` 时，游戏 `W` 可用。
- 已用无窗口测试验证设置页 `scancode` 输入和鼠标点击。
- 已用无窗口测试验证继续游戏页 `scancode` 输入和鼠标点击。

下一阶段：
- `Sprint 8：UI 组件深化`
