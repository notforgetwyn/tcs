# Sprint 9 第二小步：设置页展示当前键位配置

## 当前阶段

- 当前 Sprint：Sprint 9：输入服务抽象与可配置键位
- 本次任务：在设置页展示当前键位配置
- 下一阶段建议：Sprint 9 第三小步：增加键位修改 UI

## 当前阶段目标

- 让玩家能在设置页看到当前按键配置。
- 只做展示，不做修改键位，避免一次性引入复杂录入逻辑。
- 保持速度设置和返回主菜单功能正常。

## 本阶段完成功能

- 设置页新增 `键位说明` 区域。
- 展示移动、保存、暂停、返回等动作对应的当前键位。
- 键位数据来自 `InputService` 已加载的 `config/key_bindings.json`。
- 选中 `键位说明` 后按 `Enter/Space` 会提示：当前阶段只展示键位，修改功能后续加入。
- 鼠标点击 `键位说明` 区域可以选中该项。

## 本阶段页面与 UI 完成情况

设置页 `SettingsScene`：
- 页面标题：`设置`，使用 `TextBlock` 渲染。
- UI 组件：
  - `TextBlock`：标题、速度设置、键位说明、每行动作键位、返回主菜单、状态提示。
  - `MenuList`：继续作为设置项选中状态的数据结构。
- 速度设置项：
  - 可选中。
  - `A/D` 或左右方向键调整速度。
  - `Enter/Space` 保存到 `config/settings.json`。
- 键位说明项：
  - 可选中。
  - 展示 `move_up/move_down/move_left/move_right/save_game/pause_game/back` 对应键位。
  - `Enter/Space` 不修改键位，只显示后续功能提示。
- 返回主菜单项：
  - 可选中。
  - `Enter/Space` 或鼠标点击后返回主菜单。
- 键盘操作：
  - `W/S` 或上下方向键切换设置项。
  - `A/D` 或左右方向键只在选中速度时调整速度。
  - `Esc` 返回主菜单。
- 鼠标操作：
  - 点击速度区域选中速度。
  - 点击键位说明区域选中键位说明。
  - 点击返回主菜单区域返回主菜单。
- 状态提示：
  - 调整速度后提示 `按 Enter 保存设置。`
  - 保存速度后提示 `设置已保存。`
  - 选中键位说明确认后提示后续阶段支持修改键位。

## 本阶段完成设计

- `InputService` 新增 `binding_text(action)`，用于把动作对应键位格式化为展示文本。
- 设置页不直接读取 `config/key_bindings.json`，而是通过 `InputService` 获取已校验后的键位配置。
- 当前只展示键位，后续可以基于同一数据源增加改键 UI。

## 本阶段数据流设计

- 程序启动：`App` 创建 `InputService` -> `InputService` 读取 `config/key_bindings.json`。
- 设置页渲染：`SettingsScene.render()` -> `InputService.binding_text(action)` -> `TextBlock` 绘制键位说明。
- 速度保存：`SettingsScene` 调整 `Settings` -> `SettingsService.save()` -> 写入 `config/settings.json`。
- 键位展示：只读 `InputService.bindings`，本阶段不写 `config/key_bindings.json`。

## 本阶段核心业务场景完成进度

- 主菜单业务场景：未变更。
- 设置业务场景：完成速度设置和键位展示。
- 游戏业务场景：未变更。
- 存档业务场景：未变更。
- UI 组件化业务场景：继续使用 `TextBlock` 展示配置内容。
- 输入业务场景：完成键位配置展示入口，未完成键位修改。
- 未完成内容：键位修改、键位冲突检测、恢复默认键位按钮留到后续阶段。

## 涉及文件

- `src/core/input_service.py`
- `src/scenes/settings_scene.py`
- `docs/sprint_9_settings_key_bindings_view.md`

## 验证情况

- 需要执行语法检查。
- 需要人工验证：
  - 设置页能看到键位说明。
  - 速度设置仍能调整和保存。
  - 返回主菜单仍正常。

## 下一阶段建议

- Sprint 9 第三小步：增加键位修改 UI。
- 或者先做存档删除/命名，完善多存档管理体验。
