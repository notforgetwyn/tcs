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
- 抽离场景公共接口和基础 UI 组件，减少场景间重复代码，并修复当前部分场景文件中的中文乱码污染。

本阶段完成功能：
- 游戏主流程保持可运行
- 主菜单、设置页、提示页、游戏页改为基于共享组件渲染
- 修复相关场景中的中文文案乱码
- 修复菜单和游戏内按键响应慢的问题
- 游戏移动改为每帧轮询当前按键状态，`W/A/S/D` 和方向键响应更直接
- 菜单和设置页增加短冷却轮询，避免依赖系统按键重复导致延迟

本阶段完成设计：
- 新增 `BaseScene`，统一所有场景的接口形式
- 新增 `TextBlock`，统一文本渲染入口
- 新增 `MenuList`，统一菜单项高亮和上下移动逻辑
- `MenuScene`、`SettingsScene`、`PlaceholderScene`、`GameplayScene` 改为复用公共组件
- 场景层和 UI 辅助层的边界比之前更清晰，后续继续加按钮组件和面板组件会更顺手
- 输入处理从单纯依赖 `KEYDOWN` 调整为“事件处理 + 每帧轮询”结合，减少窗口焦点和按键重复设置带来的不稳定

涉及文件：
- `src/scenes/base_scene.py`
- `src/ui/text.py`
- `src/ui/menu_list.py`
- `src/app.py`
- `src/scenes/menu_scene.py`
- `src/scenes/placeholder_scene.py`
- `src/scenes/settings_scene.py`
- `src/scenes/gameplay_scene.py`

验证情况：
- 已通过语法检查
- 已能启动进入窗口主循环
- 已提交并推送到 GitHub

下一阶段建议：
- 继续工程优化第二小步
- 增加真正的按钮组件
- 补 `README.md` 启动说明
- 规范资源目录与后续 UI 组件结构
