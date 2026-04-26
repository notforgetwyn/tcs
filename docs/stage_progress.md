# 阶段进度记录

本文档用于按固定格式记录每个阶段的开发成果。后续每完成一个阶段，都按同样结构追加更新。

## 阶段 1：MVP 最小可运行版本

当前阶段目标：
- 先把游戏核心玩法跑起来，只做单局游戏，不引入菜单、设置、存档。

本阶段完成功能：
- 实现蛇的上下左右移动
- 实现黄色食物生成
- 实现吃到食物后加分
- 实现实时分数显示
- 实现撞墙和撞自己后游戏结束
- 支持 `R` 重新开始，`ESC` 退出或返回

本阶段完成设计：
- 建立基础工程目录，避免单文件脚本
- 确定入口层、应用层、模型层、场景层的基本边界
- 使用网格坐标管理蛇和食物，简化移动与碰撞逻辑
- 使用面向对象拆分出 `Snake`、`Food`、`GameplayScene`、`App`

涉及文件：
- `main.py`
- `requirements.txt`
- `src/app.py`
- `src/constants.py`
- `src/models/snake.py`
- `src/models/food.py`
- `src/scenes/gameplay_scene.py`

验证情况：
- 已通过语法检查
- 已能启动进入游戏主循环
- 已提交到 GitHub

下一阶段建议：
- 做主菜单系统，把启动入口从“直接开局”改成“先进入菜单”

## 阶段 2：主菜单系统

当前阶段目标：
- 增加启动首页，统一游戏入口，接入页面切换能力。

本阶段完成功能：
- 程序启动后先进入主菜单
- 主菜单支持“开始游戏 / 继续游戏 / 设置 / 退出游戏”
- 支持菜单和游戏场景切换
- `开始游戏` 可进入游戏
- `继续游戏` 和 `设置` 初始接为占位入口

本阶段完成设计：
- 把 `App` 改造成简单场景调度器
- 引入菜单场景 `MenuScene`
- 引入占位场景 `PlaceholderScene`
- 初步形成“菜单页 / 游戏页 / 设置页占位 / 继续游戏占位”的页面结构
- 页面设计和 UI 入口开始形成系统化结构

涉及文件：
- `src/app.py`
- `src/scenes/menu_scene.py`
- `src/scenes/placeholder_scene.py`
- `src/scenes/gameplay_scene.py`

验证情况：
- 已通过语法检查
- 已能启动进入菜单并切换到游戏
- 已提交到 GitHub

下一阶段建议：
- 把设置页从占位页升级成真实可用页面

## 阶段 3：设置系统

当前阶段目标：
- 让设置页可真正调节速度，并能持久化保存。

本阶段完成功能：
- 新增真实可用的设置页面
- 支持调整蛇移动速度
- 支持把设置保存到 `config/settings.json`
- 游戏启动和新开局时会读取设置并生效
- 对设置文件缺失或非法内容做默认值回退

本阶段完成设计：
- 新增 `core/file_manager.py`，统一 JSON 文件读写
- 新增 `core/settings_service.py`，统一管理设置加载与保存
- 新增 `SettingsScene` 页面
- 建立“配置服务层”的雏形
- 配置数据开始从业务逻辑里抽离，不直接散落在场景代码中

涉及文件：
- `config/settings.json`
- `src/core/file_manager.py`
- `src/core/settings_service.py`
- `src/scenes/settings_scene.py`
- `src/app.py`
- `src/scenes/gameplay_scene.py`

验证情况：
- 已通过语法检查
- 已能启动程序并进入设置页
- 已完成本地提交并推送到 GitHub

下一阶段建议：
- 做界面中文化，并开始准备存档系统

## 阶段 4：中文界面本地化

当前阶段目标：
- 把当前所有用户可见界面文案切换为中文。

本阶段完成功能：
- 窗口标题改为中文
- 主菜单改为中文
- 游戏内分数、提示、结束文案改为中文
- 设置页提示改为中文
- 占位页提示改为中文

本阶段完成设计：
- 页面文案统一转为中文语义
- 菜单、游戏页、设置页、提示页的中文 UI 文案保持一致风格
- 为后续中文化 README 和中文帮助文档打下基础

涉及文件：
- `src/constants.py`
- `src/scenes/menu_scene.py`
- `src/scenes/gameplay_scene.py`
- `src/scenes/settings_scene.py`
- `src/scenes/placeholder_scene.py`
- `src/app.py`

验证情况：
- 已通过语法检查
- 已提交并推送到 GitHub

下一阶段建议：
- 做存档系统，同时解决中文字体兼容问题

## 阶段 5：存档系统 + 中文字体修复

当前阶段目标：
- 把“继续游戏”接成真实读档入口，并解决中文显示乱码。

本阶段完成功能：
- 新增 `data/save.json`
- 游戏过程中自动保存当前进度
- 主菜单“继续游戏”可恢复上次进度
- 游戏结束时自动清除无效存档
- 修复中文界面乱码问题，优先使用支持中文的系统字体

本阶段完成设计：
- 新增 `SaveService`，统一管理存档读写
- 新增 `GameState`，统一描述可持久化游戏状态
- `App` 负责统一调度“新开游戏 / 继续游戏 / 无存档提示”
- `GameplayScene` 负责业务状态更新，不直接管理底层文件格式
- 新增 `font_manager`，统一处理字体选择和回退
- 工程结构开始形成“应用控制层 + 业务逻辑层 + 配置与存档服务层 + UI 辅助层”的清晰分工

涉及文件：
- `data/save.json`
- `src/core/save_service.py`
- `src/models/game_state.py`
- `src/app.py`
- `src/scenes/menu_scene.py`
- `src/scenes/gameplay_scene.py`
- `src/ui/font_manager.py`

验证情况：
- 已通过语法检查
- 已能启动进入窗口主循环
- 已用无窗口测试验证菜单 `W/S` 输入和游戏 `W` 转向
- 已提交并推送到 GitHub

下一阶段建议：
- 进入工程优化阶段
- 优先做场景基类、统一按钮组件、统一文本组件、README 和资源目录规范化

## 阶段 6：工程优化第一小步

当前阶段目标：
- 抽离场景公共接口和基础 UI 组件，减少场景间重复代码。
- 修复场景文件中的中文乱码污染。
- 将输入逻辑统一收敛为 `KEYDOWN` 事件处理，避免轮询和冷却时间导致交互延迟。

本阶段完成功能：
- 游戏主流程保持可运行：启动后进入主菜单，主菜单可以进入游戏、设置、继续游戏提示页或退出。
- 主菜单、设置页、提示页、游戏页改为基于共享 UI 组件渲染。
- 修复相关场景中的中文文案乱码，源码中的中文显示文案改为 Unicode 转义，降低 Windows 控制台编码污染风险。
- 修复菜单和游戏内按键响应慢的问题。
- 菜单、设置页和游戏控制全部改为纯 `KEYDOWN` 处理，不再使用 `pygame.key.get_pressed()` 轮询。
- `W/A/S/D` 和方向键都在按下瞬间响应。
- `W/A/S/D` 识别优先使用 `pygame.K_w/K_a/K_s/K_d` 物理按键码，避免中文输入法或 `event.unicode` 为空时字母键失效。

本阶段页面与 UI 完成情况：

主菜单页 `MenuScene`：
- 页面标题：`贪吃蛇`，使用 `TextBlock` 渲染。
- 菜单组件：使用 `MenuList` 渲染四个选项。
- `开始游戏`：按 `Enter` 或空格后调用 `App.start_new_game()`，清空旧存档并进入新游戏。
- `继续游戏`：按 `Enter` 或空格后调用 `App.change_scene("continue_game")`，由 `SaveService` 尝试读取存档。
- `设置`：按 `Enter` 或空格后进入 `SettingsScene`。
- `退出游戏`：按 `Enter` 或空格后调用 `App.stop()` 退出程序。
- `W/S` 与方向键：只通过 `KEYDOWN` 事件切换菜单选中项。
- 当前选中项：由 `MenuList` 用高亮颜色和 `> 选项 <` 形式显示。

设置页 `SettingsScene`：
- 页面标题：`设置`，使用 `TextBlock` 渲染。
- 速度设置项：显示当前速度等级和毫秒值，例如 `速度: 正常（140 毫秒）`。
- `W/S` 与上下方向键：通过 `KEYDOWN` 切换设置项。
- `A/D` 与左右方向键：当选中速度项时，通过 `KEYDOWN` 调整移动速度。
- `Enter` 或空格：当选中速度项时保存设置到 `config/settings.json`。
- `返回主菜单`：选中后按 `Enter` 或空格返回主菜单。
- `ESC`：直接返回主菜单。
- 状态提示：保存后显示 `设置已保存。`，调整后显示 `按 Enter 保存设置。`

提示页 `PlaceholderScene`：
- 当前用于“无可继续存档”的提示场景。
- 页面标题和提示内容使用 `TextBlock` 渲染。
- `Enter`、小键盘 `Enter` 或 `ESC`：返回主菜单。
- 该页后续可以继续扩展成正式的 `ContinueScene` 或通用消息弹窗。

游戏页 `GameplayScene`：
- HUD：显示当前分数和操作提示。
- 蛇与食物：继续使用网格绘制，蛇头、蛇身、食物颜色保持原设计。
- `W/A/S/D` 与方向键：通过 `KEYDOWN` 立即设置蛇的方向。
- 反向移动保护：仍由 `Snake.set_direction()` 控制，避免蛇直接反向撞到自己。
- `ESC`：游戏中保存当前进度并返回主菜单；游戏结束状态下清除无效存档再返回主菜单。
- `R`：游戏结束后重新开始新游戏。
- 游戏结束 UI：显示 `游戏结束`、最终分数和返回/重开提示。

本阶段完成设计：
- 新增 `BaseScene`，统一所有场景的接口形式：`handle_event()`、`update()`、`render()`。
- 新增 `TextBlock`，统一文本渲染入口，避免每个页面重复创建字体和计算居中位置。
- 新增 `MenuList`，统一菜单项渲染、高亮显示和上下移动逻辑。
- `MenuScene`、`SettingsScene`、`PlaceholderScene`、`GameplayScene` 改为复用公共组件。
- 场景层和 UI 辅助层边界更清晰：场景负责业务交互，UI 组件负责渲染细节。
- 输入处理统一使用 `KEYDOWN`，菜单切换、设置调整、游戏转向都在事件层完成。
- 字母键输入检测采用“物理按键码优先，`event.unicode` 兜底”的设计，兼容输入法状态差异。

本阶段数据流设计：
- 主菜单开始游戏数据流：`MenuScene` 接收 `KEYDOWN` -> 触发 `App.start_new_game()` -> `SaveService.clear()` 清空旧存档 -> 创建新的 `GameplayScene`。
- 主菜单继续游戏数据流：`MenuScene` 接收 `KEYDOWN` -> 触发 `App.change_scene("continue_game")` -> `SaveService.load()` 读取 `data/save.json` -> 有存档则恢复 `GameplayScene`，无存档则进入提示页。
- 设置保存数据流：`SettingsScene` 接收速度调整按键 -> 更新内存中的 `Settings` -> `Enter` 触发 `SettingsService.save()` -> 写入 `config/settings.json`。
- 游戏输入数据流：`GameplayScene.handle_event()` 接收方向键或 `W/A/S/D` -> `_direction_from_event()` 转换为方向向量 -> `Snake.set_direction()` 更新方向。
- 游戏存档数据流：游戏状态变化后由 `GameplayScene._persist_progress()` 生成 `GameState` -> `SaveService.save()` 写入 `data/save.json`。
- 游戏结束数据流：碰撞检测失败 -> `_handle_game_over()` -> `SaveService.clear()` 清除不可继续的存档。

本阶段核心业务场景完成进度：
- 主菜单业务场景：已完成开始游戏、继续游戏、设置、退出四个入口。
- 设置业务场景：已完成速度调整、速度保存、返回主菜单。
- 游戏业务场景：已完成方向输入、移动、吃食物、计分、死亡判定、结束后重开。
- 存档业务场景：本阶段未新增存档规则，只保持阶段 5 的存档/读档能力，并让主菜单继续游戏入口继续可用。
- UI 组件化业务场景：已完成文本组件和菜单组件抽离，按钮组件仍未实现。

涉及文件：
- `src/scenes/base_scene.py`
- `src/ui/text.py`
- `src/ui/menu_list.py`
- `src/app.py`
- `src/constants.py`
- `src/scenes/menu_scene.py`
- `src/scenes/placeholder_scene.py`
- `src/scenes/settings_scene.py`
- `src/scenes/gameplay_scene.py`
- `docs/stage_progress.md`

验证情况：
- 已通过语法检查：`D:\ananconda\python.exe -m compileall main.py src`
- 已确认源码中无 `get_pressed`、`NAV_COOLDOWN`、`nav_cooldown` 残留。
- 已用无窗口测试验证主菜单 `W/S` 输入。
- 已用无窗口测试验证设置页 `W/S` 输入。
- 已用无窗口测试验证游戏页 `W` 转向。
- 已用无窗口测试验证 `event.unicode` 为空时，主菜单、设置页和游戏页仍能识别 `W/S/A/D`。
- 已能启动进入窗口主循环。
- 已提交并推送到 GitHub。

下一阶段建议：
- 继续工程优化第二小步。
- 增加真正的按钮组件 `Button`，把菜单项从纯文本菜单升级为可复用 UI 控件。
- 补 `README.md`，写清楚安装依赖、启动命令、操作方式和当前阶段进度。
- 规范资源目录，为后续字体、图片、音效和主题皮肤做准备。
- 将 `ContinueScene` 从提示页拆成正式页面，展示是否存在存档、存档分数和继续/返回操作。

## 阶段 7：工程优化第二小步

当前阶段目标：
- 增加正式 `Button` UI 组件。
- 将“继续游戏”从通用提示页升级为正式 `ContinueScene`。
- 补充 `README.md`，让项目具备基础交付说明。
- 规范资源目录，为后续字体、图片、音效和主题皮肤预留位置。

本阶段完成功能：
- 新增 `Button` 组件，支持选中态、普通态、禁用态和鼠标点击命中判断。
- 新增正式 `ContinueScene` 页面。
- 主菜单点击“继续游戏”后进入 `ContinueScene`，不再直接进入通用占位页。
- 有存档时，继续游戏页显示存档摘要，并提供“继续游戏”和“返回主菜单”两个按钮。
- 无存档时，继续游戏页显示无存档提示，并只提供“返回主菜单”按钮。
- 继续游戏页支持 `W/S`、方向键、`Enter`、空格、`ESC` 和鼠标点击。
- 新增 `README.md`，记录安装依赖、启动命令、操作方式、数据文件和当前进度。
- 新增 `assets/fonts`、`assets/images`、`assets/sounds` 资源目录占位。

本阶段页面与 UI 完成情况：

继续游戏页 `ContinueScene`：
- 页面标题：`继续游戏`。
- 无存档状态：
  - 显示 `当前没有可继续的存档。`
  - 显示 `请返回主菜单开始新游戏。`
  - 显示一个按钮：`返回主菜单`
  - 按 `Enter` 或鼠标点击按钮后返回主菜单
  - 按 `ESC` 直接返回主菜单
- 有存档状态：
  - 显示 `已找到可继续的存档`
  - 显示当前分数
  - 显示蛇身长度
  - 显示当前速度毫秒值
  - 显示两个按钮：`继续游戏`、`返回主菜单`
  - 选中 `继续游戏` 后按 `Enter` 或点击按钮，恢复 `GameplayScene`
  - 选中 `返回主菜单` 后按 `Enter` 或点击按钮，返回 `MenuScene`

按钮组件 `Button`：
- 支持固定矩形区域渲染。
- 支持普通色、选中色、禁用色。
- 支持文字居中。
- 支持 `contains()` 鼠标命中检测。
- 当前已在 `ContinueScene` 中使用。
- 后续可逐步替换主菜单和设置页里的纯文本菜单项。

README 文档：
- 说明项目当前进度。
- 说明本机已验证 Python 路径。
- 说明依赖安装命令。
- 说明启动命令。
- 说明主菜单、游戏中、设置页、继续游戏页的操作方式。
- 说明 `config/settings.json` 和 `data/save.json` 的用途。

本阶段完成设计：
- 将继续游戏从 `App._continue_game()` 的直接跳转逻辑拆到独立 `ContinueScene` 页面。
- `App.change_scene("continue_game")` 现在负责创建并进入 `ContinueScene`。
- `ContinueScene` 自己读取 `SaveService.load()`，根据存档是否存在决定页面状态。
- `Button` 作为独立 UI 组件进入 `ui` 层，后续可以复用于菜单、设置、弹窗等页面。
- 资源目录拆为 `fonts/images/sounds`，避免后续资源文件直接散落在项目根目录。

本阶段数据流设计：
- 主菜单继续游戏数据流：`MenuScene` -> `App.change_scene("continue_game")` -> `ContinueScene` -> `SaveService.load()` -> 渲染有存档或无存档状态。
- 有存档恢复数据流：`ContinueScene` 选中 `继续游戏` -> `App.load_gameplay_from_state(game_state)` -> 创建带存档状态的 `GameplayScene`。
- 无存档返回数据流：`ContinueScene` 选中 `返回主菜单` 或按 `ESC` -> `App.change_scene("menu")`。
- 按钮点击数据流：鼠标点击坐标 -> `Button.contains()` -> `ContinueScene._activate_selected()` -> 执行业务动作。
- 文档交付数据流：用户拉取仓库后可通过 `README.md` 直接安装依赖并启动项目。

本阶段核心业务场景完成进度：
- 继续游戏业务场景：已从占位提示升级为正式页面。
- 存档摘要展示：已完成分数、蛇身长度、速度信息展示。
- 按钮组件化：已完成基础按钮组件，并在继续游戏页落地。
- 项目交付说明：已完成基础 README。
- 资源管理：已完成资源目录占位，尚未接入资源加载器。

涉及文件：
- `src/ui/button.py`
- `src/scenes/continue_scene.py`
- `src/app.py`
- `README.md`
- `assets/.gitkeep`
- `assets/fonts/.gitkeep`
- `assets/images/.gitkeep`
- `assets/sounds/.gitkeep`
- `docs/stage_progress.md`

验证情况：
- 已通过语法检查。
- 已用无窗口测试验证继续游戏页无存档状态。
- 已用无窗口测试验证继续游戏页有存档状态。
- 待提交并推送到 GitHub。

下一阶段建议：
- 进入 `Sprint 8：UI 组件深化`。
- 将主菜单和设置页从 `MenuList` 逐步迁移到 `Button`。
- 增加统一面板组件 `Panel`。
- 增加资源加载器，为字体、图片和音效接入做准备。
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
- `docs/stage_progress.md`

验证情况：
- 已通过语法检查：`D:\ananconda\python.exe -m compileall main.py src tools`
- 已用临时目录验证 `InputService.reset_to_defaults()` 会恢复默认键位并写入 JSON。
- 待提交并推送到 GitHub。

下一阶段建议：
- 抽象正式 `Button` UI 组件。
- 将继续游戏页、设置页、主菜单页的按钮绘制和点击命中统一收敛。
- 补充 README 当前操作说明，包括多存档、重命名、删除、恢复默认键位。
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
