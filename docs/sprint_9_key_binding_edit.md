# Sprint 9 第三小步：设置页键位修改与布局优化

## 当前阶段

- 当前 Sprint：Sprint 9：输入服务抽象与可配置键位
- 本次任务：优化设置页布局，并支持玩家修改游戏键位
- 下一阶段建议：Sprint 10：存档管理体验优化

## 当前阶段目标

- 每次启动游戏都应从主菜单开始。
- 设置页组件之间不能过于拥挤，要更清晰。
- 设置页中的键位不仅要能看，还要能改。
- 改完键位后要立即生效，并写入本地 `config/key_bindings.json`。

## 本阶段完成功能

- 设置页从原来的紧凑文本说明改为分行键位配置列表。
- 玩家可以选中某一行键位，按 `Enter/Space` 开始修改。
- 进入修改状态后，按一个支持的键即可完成绑定。
- 支持的录入键：
  - 方向键
  - A-Z 字母键
  - `Enter`
  - `Space`
  - `F3`
- `Esc` 在录入状态下表示取消修改。
- 改键后立即写入本地 `config/key_bindings.json`，并立即生效。
- 同一组游戏内可配置键位之间做冲突检测，避免两个游戏动作使用同一个键。
- `config/key_bindings.json` 和 `config/settings.json` 加入 `.gitignore`，作为用户本地配置持久化保存。
- 新增 `config/key_bindings.example.json` 和 `config/settings.example.json` 作为仓库示例配置。

## 本阶段页面与 UI 完成情况

设置页 `SettingsScene`：
- 页面标题：`设置`，使用 `TextBlock` 渲染。
- UI 组件：
  - `TextBlock`：标题、速度行、键位标题、每个键位行、返回主菜单、状态提示。
- 速度设置行：
  - 可选中。
  - `A/D` 或左右方向键调整速度。
  - `Enter/Space` 保存速度到本地 `config/settings.json`。
- 键位配置行：
  - `上移`
  - `下移`
  - `左移`
  - `右移`
  - `保存并返回菜单`
  - `暂停/继续`
  - `游戏结束后重开`
- 键位行交互：
  - 选中后按 `Enter/Space` 进入等待新按键状态。
  - 等待状态下按新键完成绑定。
  - 等待状态下按 `Esc` 取消。
  - 如果新键已被其他游戏动作使用，会显示冲突提示。
- 返回主菜单行：
  - 可选中。
  - `Enter/Space` 或鼠标点击后返回主菜单。
- 鼠标操作：
  - 鼠标悬停设置项会同步选中。
  - 鼠标点击键位行会进入改键状态。
- 状态提示：
  - 显示保存成功、等待按键、取消修改、键位冲突、修改成功等提示。

## 本阶段完成设计

- `InputService` 增加键位录入能力：
  - `capture_key_press()`
  - `sync_capture_keys()`
  - `set_single_binding(action, key_name)`
  - `action_using_key(key_name, exclude=...)`
- `KEY_NAME_TO_VK` 扩展为支持 A-Z 字母键。
- `SettingsScene` 不直接写 JSON，而是通过 `InputService.set_single_binding()` 保存键位。
- 用户本地配置与仓库示例配置分离：
  - `config/key_bindings.json`：用户本地真实键位配置。
  - `config/key_bindings.example.json`：仓库示例。
  - `config/settings.json`：用户本地速度设置。
  - `config/settings.example.json`：仓库示例。

## 本阶段数据流设计

- 启动游戏：`App.__init__()` -> `self.scene = MenuScene` -> 每次启动默认进入主菜单。
- 修改键位：`SettingsScene` 选中键位行 -> `Enter/Space` -> `capture_action` 进入等待状态 -> `InputService.capture_key_press()` 读取新键 -> `InputService.set_single_binding()` -> 写入本地 `config/key_bindings.json`。
- 使用新键位：`Scene.update()` -> `InputService.just_pressed(action)` 或 `direction()` -> 读取最新 `bindings` -> 游戏立即响应。
- 本地持久化：关闭游戏后 `config/key_bindings.json` 保留，下次启动由 `InputService._load_bindings()` 读取。

## 本阶段核心业务场景完成进度

- 主菜单业务场景：启动入口确认仍为主菜单；如果看到旧页面，通常是旧窗口进程未关闭。
- 设置业务场景：完成速度设置、键位展示、键位修改、本地持久化。
- 游戏业务场景：改键后游戏移动、保存、暂停、重开会使用新键位。
- 存档业务场景：未变更，本地 `data/save.json` 仍持久化。
- UI 组件化业务场景：设置页改为更清晰的分行布局，但尚未抽出通用设置列表组件。
- 输入业务场景：完成可配置键位第一版。
- 未完成内容：恢复默认键位按钮、键位导入导出、更多冲突策略留到后续。

## 涉及文件

- `.gitignore`
- `config/key_bindings.json`
- `config/key_bindings.example.json`
- `config/settings.json`
- `config/settings.example.json`
- `src/core/input_service.py`
- `src/scenes/settings_scene.py`
- `docs/sprint_9_key_binding_edit.md`

## 验证情况

- 需要执行语法检查。
- 需要验证 `InputService` 可以保存和读取新键位。
- 需要人工验证：
  - 每次启动默认进入主菜单。
  - 设置页布局是否更清晰。
  - 修改移动键位后，游戏中能用新键位移动。
  - 修改保存/暂停键位后，游戏中能用新键位触发。

## 下一阶段建议

- Sprint 10：存档管理体验优化。
- 增加存档删除、存档命名、恢复默认键位按钮。
