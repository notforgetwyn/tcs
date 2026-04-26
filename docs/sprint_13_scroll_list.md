## 阶段 5：工程优化 / 优化 Sprint 13：滚动列表组件抽象

当前阶段目标：
- 抽离继续游戏页中多存档列表的滚动、选中、可见项计算和边界同步逻辑。
- 让 `ContinueScene` 更专注于存档读取、重命名、删除等业务动作。
- 本阶段不修改存档 JSON 结构、游戏规则、键位系统和页面视觉风格。

本阶段完成功能：
- 新增 `ScrollList` 组件，集中管理列表选中项和滚动偏移。
- 继续游戏页接入 `ScrollList` 管理多存档列表。
- 保留滚轮浏览多存档能力。
- 保留 `W/S` 或上下方向键浏览多存档能力。
- 保留选中项离开可见范围时自动同步滚动位置。
- 保留点击存档卡片读取存档、点击重命名/删除按钮执行操作。
- 删除存档后列表会重新配置数量，并自动修正选中项和滚动偏移。

本阶段页面与 UI 完成情况：

继续游戏页 `ContinueScene`：
- 页面标题：`继续游戏`，仍由 `TextBlock` 渲染。
- UI 组件：继续使用 `SaveCard`、`Button`、`Panel`、`TextBlock`，新增接入 `ScrollList`。
- 存档列表：由 `ScrollList.visible_items()` 提供当前可见存档，页面负责把每个可见项渲染成 `SaveCard`。
- 滚动状态：由 `ScrollList.scroll_status()` 提供显示范围，例如 `显示 1-5 / 8`。
- `重命名` 按钮：点击后继续调用 `_start_rename()`，业务不变。
- `删除` 按钮：点击后继续调用 `_request_or_confirm_delete()`，业务不变。
- `返回主菜单` 按钮：仍使用 `Button`，选中索引仍位于存档列表之后。
- 键盘操作：`W/S` 或上下方向键调用 `ScrollList.move_selection()`，`Enter` 读取或返回，`N` 重命名，`Delete` 删除，`Esc` 返回或取消。
- 鼠标操作：滚轮调用 `ScrollList.scroll()`；鼠标悬停和点击仍能更新当前选中项。

滚动列表组件 `ScrollList`：
- `configure()`：设置列表数量和额外可选项数量，并修正越界状态。
- `move_selection()`：处理上下移动和循环选择。
- `scroll()`：处理滚轮滚动，并让选中项保持在可见范围内。
- `visible_items()`：返回当前可见项的真实索引和数据。
- `scroll_status()`：返回当前显示范围和总数量。
- `sync_to_selection()`：当选中项改变时同步滚动偏移。

本阶段完成设计：
- 新增 `src/ui/scroll_list.py`，将滚动状态管理从场景层抽离到 UI 状态组件。
- `ContinueScene` 删除旧的 `_sync_scroll_to_selection()`、`_last_index()` 和不再使用的 `_visible_slots()`。
- `ContinueScene` 不再直接维护 `scroll_offset`，改由 `ScrollList.scroll_offset` 管理。
- `ContinueScene` 不再直接维护 `selected_index`，改由 `ScrollList.selected_index` 管理。
- 继续游戏页的业务动作仍留在场景层，滚动列表组件只负责通用列表状态，不感知存档业务。

本阶段数据流设计：
- 进入继续游戏页数据流：`ContinueScene.on_enter()` -> `SaveService.list_saves()` -> `ScrollList.configure(len(save_slots), extra_selectable_count=1)`。
- 渲染存档列表数据流：`ContinueScene.render()` -> `ScrollList.visible_items(save_slots)` -> `SaveCard.draw()`。
- 键盘浏览数据流：`InputService.just_pressed("menu_up/menu_down")` -> `ContinueScene._move_selection()` -> `ScrollList.move_selection()` -> 自动同步可见范围。
- 鼠标滚轮数据流：`pygame.MOUSEWHEEL` -> `ContinueScene._scroll()` -> `ScrollList.scroll()` -> 更新 `scroll_offset` 和 `selected_index`。
- 删除存档数据流：`SaveService.delete()` -> `SaveService.list_saves()` -> `ScrollList.configure()` -> 修正选中项和滚动偏移。
- 点击读取数据流：鼠标坐标 -> `ContinueScene._hit_test()` -> `ScrollList.visible_items()` 对应真实索引 -> `App.load_gameplay_from_state()`。

本阶段核心业务场景完成进度：
- 主菜单业务场景：本阶段未改动，保持按钮化入口。
- 设置业务场景：本阶段未改动，保持速度、键位修改和恢复默认键位能力。
- 游戏业务场景：本阶段未改动，移动、暂停、保存、计分、死亡判定保持原逻辑。
- 存档业务场景：多存档列表滚动状态完成组件化，读取、重命名、删除业务保持稳定。
- UI 组件化业务场景：新增 `ScrollList`，继续推进“页面负责业务、组件负责通用 UI 状态”的结构。
- 输入业务场景：本阶段未改动 Windows 系统级兜底输入。
- 未完成内容：滚动列表当前只管理状态，尚未抽象滚动条视觉；后续可增加 `ScrollBar` 或列表容器组件。

涉及文件：
- `src/ui/scroll_list.py`
- `src/scenes/continue_scene.py`
- `docs/sprint_13_scroll_list.md`
- `docs/stage_progress.md`

验证情况：
- 已通过语法检查：`D:\ananconda\python.exe -m compileall main.py src tools`
- 已用脚本验证 `ScrollList` 的可见项、滚动、循环选择和删除后边界修正。
- 待提交并推送到 GitHub。

下一阶段建议：
- 继续优化 README，补齐当前多存档、重命名、删除、设置键位、恢复默认键位的操作说明。
- 或进入主题系统小步，把按钮、卡片、面板颜色集中管理。
