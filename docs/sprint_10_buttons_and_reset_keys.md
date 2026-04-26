## 阶段 10：存档操作按钮与键位恢复默认

当前阶段目标：
- 将继续游戏页的存档管理从“只靠键盘快捷键”升级为“键盘 + 鼠标按钮”都可操作。
- 在设置页增加恢复默认键位能力，避免用户改错键位后无法快速回到可用配置。
- 本阶段不改变核心蛇移动、食物生成、计分、存档结构，只优化存档管理和设置体验。

本阶段完成功能：
- 继续游戏页每个存档卡片右侧新增 `重命名` 按钮。
- 继续游戏页每个存档卡片右侧新增 `删除` 按钮。
- 鼠标点击 `重命名` 后进入重命名输入状态，输入新名称后按 `Enter` 保存。
- 鼠标点击 `删除` 后进入二次确认状态，再点击同一存档的 `删除` 或按 `Delete` 完成删除。
- 原有键盘操作保留：`Enter` 读取存档，`N` 重命名，`Delete` 删除，`Esc` 返回或取消。
- 设置页新增 `恢复默认键位` 菜单项，选中后按 `Enter` 或鼠标点击即可恢复默认键位。
- 恢复默认键位后立即写入 `config/key_bindings.json`，并立刻生效。

本阶段页面与 UI 完成情况：

继续游戏页 `ContinueScene`：
- 页面标题：`继续游戏`，继续使用 `TextBlock` 渲染。
- UI 组件：继续使用 `TextBlock` 绘制标题、提示、存档卡片文本和状态栏。
- 存档卡片：仍显示存档序号、存档名、分数、蛇长度、更新时间。
- `重命名` 按钮：每个存档卡片右侧绿色按钮，鼠标点击后调用 `_start_rename()`，进入重命名状态。
- `删除` 按钮：每个存档卡片右侧红色按钮，鼠标点击后调用 `_request_or_confirm_delete()`，第一次点击提示确认，第二次确认删除。
- 卡片点击：点击卡片主体仍然读取该存档并进入游戏页。
- 键盘操作：`W/S` 或上下方向键切换选中项，`Enter` 读取，`N` 重命名，`Delete` 删除，`Esc` 返回或取消删除。
- 鼠标操作：移动鼠标会高亮卡片，点击按钮执行对应动作，滚轮继续浏览多存档列表。
- 状态提示：底部显示读取、重命名、删除确认、取消、删除完成等提示。

设置页 `SettingsScene`：
- 页面标题：`设置`，继续使用 `TextBlock` 渲染。
- UI 组件：继续使用文本菜单式 UI，当前阶段未引入独立 `Button` 类。
- 速度设置项：保持原有 `A/D` 或左右方向键调整，`Enter` 保存速度。
- 键位设置项：保持原有选中后按 `Enter` 进入捕获模式，再按新键完成绑定。
- `恢复默认键位` 菜单项：新增在键位列表下方，选中后按 `Enter` 或鼠标点击触发 `InputService.reset_to_defaults()`。
- `返回主菜单` 菜单项：位置下移，选中后按 `Enter` 或鼠标点击返回主菜单。
- 键盘操作：`W/S` 或上下方向键切换设置项，`Enter` 执行动作，`Esc` 返回主菜单或取消键位捕获。
- 鼠标操作：鼠标点击速度、键位、恢复默认、返回菜单等行会先选中再执行。
- 状态提示：恢复默认后显示 `已恢复默认键位，立即生效。`

本阶段完成设计：
- `ContinueScene` 新增 `_save_action_rects()`，统一计算每个存档卡片内的操作按钮区域。
- `ContinueScene` 新增 `_draw_save_action_buttons()`，把重命名和删除按钮的绘制从卡片主体绘制中拆出来。
- `ContinueScene` 新增 `_hit_test_action()`，优先判断鼠标是否点中操作按钮，避免按钮点击误触发读取存档。
- `SettingsScene` 新增 `_reset_index()` 和 `_draw_reset_row()`，将恢复默认键位作为正式设置项纳入页面选择流。
- `InputService` 新增 `reset_to_defaults()`，集中处理默认键位恢复和 JSON 持久化，避免设置页直接操作底层文件。
- 场景层继续负责页面交互，输入服务层负责键位配置读写，文件存储层继续通过 JSON 保存运行配置。

本阶段数据流设计：
- 存档重命名按钮数据流：`ContinueScene` 鼠标点击 `重命名` -> `_hit_test_action()` 命中按钮 -> `_start_rename()` -> 用户输入新名称 -> `_confirm_rename()` -> `SaveService.rename()` -> 写入 `data/save.json`。
- 存档删除按钮数据流：`ContinueScene` 鼠标点击 `删除` -> `_request_or_confirm_delete()` 进入确认状态 -> 第二次确认 -> `SaveService.delete()` -> 更新 `data/save.json` -> 刷新存档列表。
- 存档读取数据流：`ContinueScene` 点击卡片主体或按 `Enter` -> `_activate_selected()` -> `App.load_gameplay_from_state()` -> 切换到 `GameplayScene`。
- 恢复默认键位数据流：`SettingsScene` 选中 `恢复默认键位` -> `_activate_selected()` -> `InputService.reset_to_defaults()` -> 写入 `config/key_bindings.json` -> 同步按键边沿状态 -> 页面提示立即生效。

本阶段核心业务场景完成进度：
- 主菜单业务场景：本阶段未改动，仍保持开始游戏、继续游戏、设置、退出入口。
- 设置业务场景：新增恢复默认键位，键位改错后的可恢复能力完成。
- 游戏业务场景：本阶段未改动，游戏移动、暂停、保存、计分、死亡判定保持原逻辑。
- 存档业务场景：在多存档读取、删除、重命名基础上，补齐鼠标按钮操作入口。
- UI 组件化业务场景：本阶段仍使用 `TextBlock` 和场景内部矩形按钮，正式 `Button` 类留到后续 UI 组件化阶段。
- 输入业务场景：不改变 Windows 系统级输入读取方案，只新增默认键位恢复能力。
- 未完成内容：后续仍建议抽象真正的 `Button` 组件，并统一菜单、设置、存档页的按钮样式与点击行为。

涉及文件：
- `src/core/input_service.py`
- `src/scenes/continue_scene.py`
- `src/scenes/settings_scene.py`
- `docs/sprint_10_buttons_and_reset_keys.md`

验证情况：
- 已通过语法检查：`D:\ananconda\python.exe -m compileall main.py src tools`
- 已用临时目录验证 `InputService.reset_to_defaults()` 会恢复默认键位并写入 JSON。
- 待提交并推送到 GitHub。

下一阶段建议：
- 抽象正式 `Button` UI 组件。
- 将继续游戏页、设置页、主菜单页的按钮绘制和点击命中统一收敛。
- 补充 README 当前操作说明，包括多存档、重命名、删除、恢复默认键位。
