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
- 已能启动进入窗口主循环。
- 已提交并推送到 GitHub。

下一阶段建议：
- 继续工程优化第二小步。
- 增加真正的按钮组件 `Button`，把菜单项从纯文本菜单升级为可复用 UI 控件。
- 补 `README.md`，写清楚安装依赖、启动命令、操作方式和当前阶段进度。
- 规范资源目录，为后续字体、图片、音效和主题皮肤做准备。
- 将 `ContinueScene` 从提示页拆成正式页面，展示是否存在存档、存档分数和继续/返回操作。
