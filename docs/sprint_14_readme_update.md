## 阶段 5：工程优化 / 优化 Sprint 14：README 操作说明补齐

当前阶段目标：
- 修复 README 中的中文乱码污染。
- 将 README 从旧的 Sprint 9 状态更新到当前真实项目状态。
- 补齐启动方式、页面操作、存档管理、键位设置、数据文件和架构说明。
- 本阶段只更新文档，不修改游戏代码和 JSON 数据结构。

本阶段完成功能：
- 重写 `README.md`，恢复正常中文显示。
- 更新当前进度为 `阶段 5：工程优化 / 优化 Sprint 14：README 操作说明补齐`。
- 补充当前已完成功能列表，包括多存档、重命名、删除、恢复默认键位、UI 组件化和 Windows 系统级输入。
- 补充安装依赖命令和启动游戏命令。
- 补充主菜单、游戏中、继续游戏页、设置页的完整操作说明。
- 补充默认键位表。
- 补充输入系统链路说明。
- 补充运行时 JSON 文件和 example JSON 文件说明。
- 补充项目目录结构和分层架构图。
- 更新项目文档索引到 Sprint 13。

本阶段页面与 UI 完成情况：

主菜单页 `MenuScene`：
- README 已说明 `开始游戏`、`继续游戏`、`设置`、`退出游戏` 四个按钮。
- README 已说明 `W/S`、方向键、`Enter`、`Space`、鼠标点击、`Esc` 的响应结果。

游戏页 `GameplayScene`：
- README 已说明 `W/A/S/D`、方向键、`E`、`P`、`Esc`、`R` 的作用。
- README 已说明吃黄色方块加分、撞墙或撞自己游戏结束。
- README 已说明游戏中保存后返回主菜单，后续从继续游戏页读取。

继续游戏页 `ContinueScene`：
- README 已说明页面读取 `data/save.json` 中的所有本地存档。
- README 已说明存档卡片显示序号、存档名、分数、蛇长度、最后更新时间。
- README 已说明键盘浏览、鼠标滚轮浏览、读取存档、重命名、删除和返回主菜单。
- README 已说明重命名状态下 `Enter`、`Backspace`、`Esc` 的行为。
- README 已说明存档名不能为空且最长 24 个字符。

设置页 `SettingsScene`：
- README 已说明速度调整和保存方式。
- README 已说明键位修改流程和取消方式。
- README 已说明 `恢复默认键位` 的操作方式。
- README 已说明可修改的键位范围。

本阶段完成设计：
- README 从“阶段说明文档”升级为“玩家和开发者入口文档”。
- 文档结构按使用顺序组织：当前进度 -> 环境 -> 安装 -> 启动 -> 操作 -> 输入系统 -> 数据文件 -> 项目结构 -> 项目文档。
- README 中的架构图使用项目约定的分层框图格式。
- README 明确区分运行时本地 JSON 和仓库 example JSON，降低误提交存档和配置的风险。
- 本阶段没有新增代码模块，属于交付文档质量优化。

本阶段数据流设计：
- 启动说明数据流：用户执行启动命令 -> `main.py` -> `App` 初始化 -> 默认进入 `MenuScene`。
- 存档说明数据流：游戏中保存 -> `SaveService` 写入 `data/save.json` -> 继续游戏页读取并展示所有存档。
- 设置说明数据流：设置页调整速度或键位 -> `SettingsService` 或 `InputService` 写入 `config/*.json` -> 下次启动继续生效。
- 输入说明数据流：`config/key_bindings.json` -> `InputService` -> `system_keys.GetAsyncKeyState` -> 场景层响应动作。

本阶段核心业务场景完成进度：
- 主菜单业务场景：文档说明已补齐。
- 设置业务场景：文档说明已补齐。
- 游戏业务场景：文档说明已补齐。
- 存档业务场景：文档说明已补齐。
- UI 组件化业务场景：README 已记录当前组件化结果。
- 输入业务场景：README 已说明 Windows 系统级输入链路。
- 未完成内容：README 后续可继续补充截图、发布包说明和常见问题。

涉及文件：
- `README.md`
- `docs/sprint_14_readme_update.md`
- `docs/stage_progress.md`

验证情况：
- 已检查 README，不再包含明显乱码片段或旧的 Sprint 9 当前进度。
- 已通过语法检查：`D:\ananconda\python.exe -m compileall main.py src tools`
- 待提交并推送到 GitHub。

下一阶段建议：
- 进入主题系统小步，把按钮、卡片、面板颜色集中管理。
- 或补充 FAQ 和截图说明，提升项目交付完整度。
