# Sprint 9 补充：本地存档持久化规则修正

## 当前阶段

- 当前 Sprint：Sprint 9：输入服务抽象与可配置键位
- 本次补充任务：确保玩家本地存档不会被 Git 提交或后续开发重置
- 下一阶段建议：Sprint 9 第二小步：设置页展示当前键位配置

## 当前阶段目标

- 玩家本次玩游戏产生的存档，关闭游戏后下一次启动仍然可以看到。
- `data/save.json` 作为运行时本地数据保留在玩家机器上。
- Git 仓库不再跟踪真实运行存档，避免开发提交时把玩家存档重置成空数据。

## 本阶段完成功能

- `data/save.json` 加入 `.gitignore`。
- `data/save.json` 将从 Git 跟踪中移除，但本地文件继续保留。
- 新增 `data/save.example.json`，用于说明存档 JSON 的默认结构。
- README 增加说明：真实存档是本地运行时文件，不提交到 Git。

## 本阶段页面与 UI 完成情况

继续游戏页 `ContinueScene`：
- 页面标题：`继续游戏`，继续使用 `TextBlock` 渲染。
- UI 组件：多个存档 `Button`、返回主菜单 `Button`。
- 存档按钮：读取本地 `data/save.json` 中的多个存档槽。
- 键盘操作：`W/S` 或方向键选择存档，`Enter/Space` 读取。
- 鼠标操作：悬停高亮，点击读取。
- 状态提示：没有存档时显示无存档提示。

## 本阶段完成设计

- 将真实运行数据和仓库示例数据分离。
- `data/save.json`：本地真实存档，只在玩家电脑上保存。
- `data/save.example.json`：仓库示例文件，用于说明默认结构。
- `FileManager.load_json()` 已具备文件不存在时自动创建默认 JSON 的能力，因此移除 Git 跟踪不会影响程序运行。

## 本阶段数据流设计

- 游戏中保存：`GameplayScene._persist_progress()` -> `SaveService.save()` -> 写入本地 `data/save.json`。
- 关闭游戏：本地 `data/save.json` 保留在磁盘上。
- 下次启动：`ContinueScene` -> `SaveService.list_saves()` -> 读取本地 `data/save.json` -> 展示多个存档按钮。
- Git 提交：`.gitignore` 忽略 `data/save.json`，不会把玩家存档提交到仓库。

## 本阶段核心业务场景完成进度

- 主菜单业务场景：未变更。
- 设置业务场景：未变更。
- 游戏业务场景：保存逻辑保持不变。
- 存档业务场景：完成本地运行存档与 Git 仓库数据分离。
- UI 组件化业务场景：未变更。
- 输入业务场景：未变更。
- 未完成内容：后续可增加存档删除、命名、导入导出。

## 涉及文件

- `.gitignore`
- `data/save.json`
- `data/save.example.json`
- `README.md`
- `docs/sprint_9_persistent_save_storage.md`

## 验证情况

- 需要验证 `data/save.json` 从 Git 跟踪中移除但本地仍存在。
- 需要验证 Git 状态不再显示运行时存档修改。
- 需要验证程序仍可读取本地存档。

## 下一阶段建议

- 继续 `Sprint 9 第二小步`：设置页展示当前键位配置。
