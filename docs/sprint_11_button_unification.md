## 阶段 11：按钮组件统一第一小步

当前阶段目标：
- 将主菜单和部分高频操作入口统一迁移到 `Button` 组件。
- 减少页面中手写矩形按钮、手写边框和手写点击命中逻辑。
- 本阶段只做低风险 UI 组件化，不改动存档结构、游戏规则和 Windows 系统级输入方案。

本阶段完成功能：
- 主菜单四个入口全部改为真正的 `Button` 组件渲染。
- 主菜单支持鼠标悬停高亮，鼠标点击按钮后执行对应菜单动作。
- 主菜单保留键盘操作：`W/S` 或上下方向键切换，`Enter` 或空格确认。
- 继续游戏页的 `重命名`、`删除` 小按钮改为复用 `Button` 组件。
- 继续游戏页的 `返回主菜单` 按钮改为复用 `Button` 组件。
- 设置页的 `恢复默认键位` 和 `返回主菜单` 改为复用 `Button` 组件。
- 原有存档读取、删除二次确认、重命名、恢复默认键位能力保持不变。

本阶段页面与 UI 完成情况：

主菜单页 `MenuScene`：
- 页面标题：`贪吃蛇`，继续使用 `TextBlock` 渲染。
- UI 组件：四个菜单入口从 `MenuList` 文本菜单迁移到 `Button`。
- `开始游戏` 按钮：鼠标点击或键盘确认后调用 `App.start_new_game()`，创建新存档并进入游戏。
- `继续游戏` 按钮：鼠标点击或键盘确认后调用 `App.change_scene("continue_game")`，进入继续游戏页。
- `设置` 按钮：鼠标点击或键盘确认后调用 `App.change_scene("settings")`。
- `退出游戏` 按钮：鼠标点击或键盘确认后调用 `App.stop()`。
- 键盘操作：`W/S` 或上下方向键切换按钮，`Enter` 或空格确认。
- 鼠标操作：移动到按钮上会更新高亮和当前选中项，点击后执行按钮动作。
- 状态提示：底部继续显示操作提示。

继续游戏页 `ContinueScene`：
- 页面标题：`继续游戏`，继续使用 `TextBlock` 渲染。
- UI 组件：存档卡片仍为场景自绘；卡片内 `重命名`、`删除` 操作按钮改为 `Button`。
- `重命名` 按钮：点击后进入重命名模式，仍由 `_start_rename()` 处理。
- `删除` 按钮：点击后进入或完成删除确认，仍由 `_request_or_confirm_delete()` 处理。
- `返回主菜单` 按钮：改为 `Button` 组件，鼠标点击或键盘选中确认后返回主菜单。
- 键盘操作：保留 `Enter` 读取、`N` 重命名、`Delete` 删除、`Esc` 返回或取消。
- 鼠标操作：按钮命中仍优先于卡片主体命中，避免点击按钮时误读取存档。
- 状态提示：底部继续显示读取、重命名、删除确认、删除完成等状态。

设置页 `SettingsScene`：
- 页面标题：`设置`，继续使用 `TextBlock` 渲染。
- UI 组件：速度项和键位项仍使用文本行；底部 `恢复默认键位`、`返回主菜单` 改为 `Button`。
- `恢复默认键位` 按钮：点击或键盘确认后调用 `InputService.reset_to_defaults()`，恢复默认键位并写入 `config/key_bindings.json`。
- `返回主菜单` 按钮：点击或键盘确认后调用 `App.change_scene("menu")`。
- 键盘操作：`W/S` 或上下方向键仍可在速度、键位、恢复默认、返回之间切换。
- 鼠标操作：点击恢复默认或返回按钮会先选中再执行。
- 状态提示：恢复默认后显示 `已恢复默认键位，立即生效。`

本阶段完成设计：
- `MenuScene` 去掉对 `MenuList` 的依赖，改为通过 `_button_rect()` 生成按钮区域。
- `MenuScene` 新增 `selected_index` 和 `hovered_index`，让键盘选中态和鼠标悬停态都能映射到 `Button.draw()`。
- `ContinueScene` 复用 `Button` 绘制存档操作按钮和返回按钮，保留存档卡片自绘能力。
- `SettingsScene` 复用 `Button` 绘制底部动作入口，速度和键位列表暂不重构，降低本阶段风险。
- UI 层边界进一步清晰：按钮的颜色、边框、文本居中、禁用态和命中检测由 `Button` 负责；页面只负责业务动作。
- 本阶段是 UI 组件化第一小步，后续可以继续将设置行和存档卡片抽象为更高级组件。

本阶段数据流设计：
- 主菜单开始游戏数据流：`MenuScene` 鼠标点击或键盘确认 `开始游戏` -> `_activate_selected()` -> `App.start_new_game()` -> 创建新 `GameplayScene`。
- 主菜单继续游戏数据流：`MenuScene` 点击 `继续游戏` -> `App.change_scene("continue_game")` -> `ContinueScene.on_enter()` -> `SaveService.list_saves()` 读取 `data/save.json`。
- 存档按钮数据流：`ContinueScene` 点击卡片内按钮 -> `_hit_test_action()` 命中动作 -> `Button` 负责视觉，场景负责调用 `_start_rename()` 或 `_request_or_confirm_delete()`。
- 设置恢复默认数据流：`SettingsScene` 点击 `恢复默认键位` -> `_activate_selected()` -> `InputService.reset_to_defaults()` -> 写入 `config/key_bindings.json`。
- 返回主菜单数据流：`ContinueScene` 或 `SettingsScene` 点击 `返回主菜单` -> `App.change_scene("menu")`。

本阶段核心业务场景完成进度：
- 主菜单业务场景：四个入口完成按钮化，键盘和鼠标操作都可用。
- 设置业务场景：底部动作入口按钮化，速度和键位行仍保持文本行实现。
- 游戏业务场景：本阶段未改动，移动、暂停、保存、计分、死亡判定保持原逻辑。
- 存档业务场景：存档卡片内操作按钮完成组件复用，读取、删除、重命名逻辑保持稳定。
- UI 组件化业务场景：已完成主菜单按钮化和两个页面的动作按钮复用；设置行、存档卡片、通用面板仍待后续抽象。
- 输入业务场景：本阶段未改动输入服务，继续使用 Windows 系统级兜底输入。
- 未完成内容：正式抽象 `Panel`、`SaveCard`、`SettingRow` 组件留到后续 Sprint。

涉及文件：
- `src/scenes/menu_scene.py`
- `src/scenes/continue_scene.py`
- `src/scenes/settings_scene.py`
- `docs/sprint_11_button_unification.md`
- `docs/stage_progress.md`

验证情况：
- 已通过语法检查：`D:\ananconda\python.exe -m compileall main.py src tools`
- 待提交并推送到 GitHub。

下一阶段建议：
- 抽象 `Panel` 组件，统一弹窗、设置页和继续游戏页的背景容器。
- 抽象 `SaveCard` 组件，继续游戏页只保留业务动作，不再直接绘制卡片细节。
- 抽象 `SettingRow` 组件，让速度项和键位项也进入统一 UI 体系。
