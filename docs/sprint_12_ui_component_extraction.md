## 阶段 12：UI 组件抽象第一小步

当前阶段目标：
- 把继续游戏页和设置页中重复的绘制逻辑抽离为可复用 UI 组件。
- 降低场景层对矩形绘制、文本行绘制、卡片按钮命中的直接依赖。
- 本阶段只做 UI 层结构优化，不修改游戏规则、存档 JSON 结构、键位 JSON 结构和 Windows 系统级输入方案。

本阶段完成功能：
- 新增 `Panel` 组件，用于绘制圆角面板和边框。
- 新增 `SaveCard` 组件，用于绘制单个存档卡片、存档摘要和卡片内操作按钮。
- 新增 `SettingRow` 组件，用于绘制设置页中的可选中文本行。
- 继续游戏页的存档卡片绘制迁移到 `SaveCard`。
- 继续游戏页的重命名输入面板背景迁移到 `Panel`。
- 设置页的速度行和键位行迁移到 `SettingRow`。
- 原有鼠标点击、键盘选择、存档读取、存档重命名、删除确认、恢复默认键位功能保持不变。

本阶段页面与 UI 完成情况：

继续游戏页 `ContinueScene`：
- 页面标题：`继续游戏`，仍由 `TextBlock` 渲染。
- UI 组件：新增接入 `SaveCard`、`Panel`、`Button`、`TextBlock`。
- 存档卡片：由 `SaveCard.draw()` 绘制，显示存档序号、名称、分数、蛇长度、更新时间。
- `重命名` 按钮：由 `SaveCard` 内部创建 `Button`，点击后仍由 `ContinueScene._start_rename()` 执行业务。
- `删除` 按钮：由 `SaveCard` 内部创建 `Button`，点击后仍由 `ContinueScene._request_or_confirm_delete()` 执行业务。
- `返回主菜单` 按钮：继续使用 `Button` 组件。
- 重命名面板：背景和边框由 `Panel` 绘制，输入文案仍由 `TextBlock` 绘制。
- 鼠标操作：`SaveCard.action_at()` 判断是否点中卡片内按钮；卡片主体点击仍读取存档。
- 键盘操作：`Enter` 读取，`N` 重命名，`Delete` 删除，`Esc` 返回或取消，保持不变。

设置页 `SettingsScene`：
- 页面标题：`设置`，仍由 `TextBlock` 渲染。
- UI 组件：新增接入 `SettingRow`、`Button`、`TextBlock`。
- 速度设置行：由 `SettingRow` 绘制，选中时显示高亮和 `> <` 标识。
- 键位设置行：由 `SettingRow` 绘制，显示动作名称和当前绑定键位。
- `恢复默认键位` 按钮：继续使用 `Button` 组件。
- `返回主菜单` 按钮：继续使用 `Button` 组件。
- 鼠标操作：`SettingRow.contains()` 用于判断速度行和键位行点击命中。
- 键盘操作：`W/S` 或上下方向键切换，`A/D` 或左右方向键调速度，`Enter` 执行动作，保持不变。

本阶段完成设计：
- 新增 `src/ui/panel.py`，封装通用圆角面板绘制。
- 新增 `src/ui/save_card.py`，封装存档卡片的视觉结构和按钮命中判断。
- 新增 `src/ui/setting_row.py`，封装设置页可选择文本行的绘制和命中区域。
- `ContinueScene` 不再直接绘制存档卡片内部文本和按钮，只负责把 `SaveSlot` 转换为 `SaveCard` 并处理业务动作。
- `SettingsScene` 不再直接拼接速度行和键位行的选中样式，只负责提供 label/value 和处理业务动作。
- UI 层负责视觉与命中，场景层负责状态与业务，边界比上个 Sprint 更清晰。

本阶段数据流设计：
- 存档卡片绘制数据流：`ContinueScene` 从 `SaveService.list_saves()` 获取 `SaveSlot` -> `_save_card()` 创建 `SaveCard` -> `SaveCard.draw()` 渲染卡片。
- 存档卡片按钮数据流：鼠标点击坐标 -> `ContinueScene._hit_test_action()` -> `SaveCard.action_at()` -> 返回 `rename/delete` -> 场景调用对应业务方法。
- 重命名面板数据流：`ContinueScene` 进入重命名状态 -> `Panel.draw()` 绘制背景 -> `TextBlock` 显示当前输入 -> `_confirm_rename()` 写入 `data/save.json`。
- 设置行绘制数据流：`SettingsScene` 生成 label/value -> `SettingRow.draw()` 渲染行 -> 用户通过键盘或鼠标选中 -> `_activate_selected()` 执行业务。
- 设置行点击数据流：鼠标坐标 -> `SettingRow.contains()` -> 返回行索引 -> `SettingsScene` 更新 `selected_index`。

本阶段核心业务场景完成进度：
- 主菜单业务场景：本阶段未改动，保持阶段 11 的按钮化结果。
- 设置业务场景：速度行和键位行完成组件化，恢复默认键位和返回主菜单保持按钮化。
- 游戏业务场景：本阶段未改动，移动、暂停、保存、计分、死亡判定保持原逻辑。
- 存档业务场景：存档卡片完成组件化，读取、重命名、删除确认逻辑保持稳定。
- UI 组件化业务场景：新增 `Panel`、`SaveCard`、`SettingRow`，继续推进从页面内绘制到组件化绘制。
- 输入业务场景：本阶段未改动输入服务，继续使用 Windows 系统级兜底输入。
- 未完成内容：后续可以继续抽象页面布局、主题系统和滚动列表组件。

涉及文件：
- `src/ui/panel.py`
- `src/ui/save_card.py`
- `src/ui/setting_row.py`
- `src/scenes/continue_scene.py`
- `src/scenes/settings_scene.py`
- `docs/sprint_12_ui_component_extraction.md`
- `docs/stage_progress.md`

验证情况：
- 已通过语法检查：`D:\ananconda\python.exe -m compileall main.py src tools`
- 待提交并推送到 GitHub。

下一阶段建议：
- 抽象滚动列表组件，统一继续游戏页多存档列表的滚动、选中和命中逻辑。
- 引入主题配置，把按钮颜色、面板颜色、卡片颜色集中管理。
- 补充 README 的当前操作说明和阶段进度。
