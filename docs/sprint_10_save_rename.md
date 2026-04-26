# Sprint 10 第二小步：手动重命名存档

## 当前阶段

- 当前 Sprint：Sprint 10：存档管理体验优化
- 本次任务：继续游戏页支持手动重命名存档
- 下一阶段建议：Sprint 10 第三小步：存档管理按钮化与恢复默认键位

## 当前阶段目标

- 玩家可以给存档起更容易识别的名字。
- 重命名要直接写入本地 `data/save.json`。
- 重命名过程要有清晰提示，并支持取消。

## 本阶段完成功能

- 继续游戏页选中存档后按 `N` 进入重命名模式。
- 重命名模式下可以直接输入新名称。
- `Backspace` 删除一个字符。
- `Enter/Space` 保存新名称。
- `Esc` 取消重命名。
- 存档名称最长限制为 24 个字符，避免 UI 溢出。
- 保存后继续游戏页立即刷新存档名称。

## 本阶段页面与 UI 完成情况

继续游戏页 `ContinueScene`：
- 页面标题：`继续游戏`，使用 `TextBlock` 渲染。
- UI 组件：
  - `TextBlock`：标题、滚动提示、存档卡片文字、重命名面板、底部状态提示。
  - 自绘存档卡片：显示存档名称和摘要。
- 存档卡片：
  - `Enter/Space` 读取。
  - `N` 进入重命名。
  - `Delete` 二次确认删除。
- 重命名面板：
  - 显示 `输入新存档名：`。
  - 显示当前输入中的新名称。
  - `Enter/Space` 保存。
  - `Esc` 取消。
  - `Backspace` 删除字符。
- 鼠标操作：
  - 悬停高亮。
  - 点击读取。
  - 滚轮浏览更多存档。

## 本阶段完成设计

- `InputService` 新增 `rename_save` 动作，默认键位为 `N`。
- `InputService` 新增 `rename_backspace` 动作，默认键位为 `BACKSPACE`。
- `ContinueScene` 新增：
  - `rename_save_id`
  - `rename_buffer`
  - `_start_rename()`
  - `_update_rename_mode()`
  - `_confirm_rename()`
  - `_cancel_rename()`
- 重命名文本输入使用 Pygame `TEXTINPUT`，但保存逻辑仍通过 `SaveService.rename()` 写入 JSON。

## 本阶段数据流设计

- 进入重命名：选中存档 -> 按 `N` -> `ContinueScene._start_rename()` -> 记录 `rename_save_id` 和 `rename_buffer`。
- 输入文本：`pygame.TEXTINPUT` -> `_append_rename_text()` -> 更新 `rename_buffer`。
- 保存名称：`Enter/Space` -> `_confirm_rename()` -> `SaveService.rename(save_id, name)` -> 写入本地 `data/save.json` -> `SaveService.list_saves()` 刷新列表。
- 取消名称：`Esc` -> `_cancel_rename()` -> 丢弃 `rename_buffer`。

## 本阶段核心业务场景完成进度

- 主菜单业务场景：未变更。
- 设置业务场景：未变更。
- 游戏业务场景：未变更。
- 存档业务场景：完成存档自动命名、删除、手动重命名。
- UI 组件化业务场景：重命名面板先在 `ContinueScene` 内实现，后续可抽成弹窗组件。
- 输入业务场景：新增 `N` 和 `Backspace` 两个存档管理动作。
- 未完成内容：按钮化删除/重命名、恢复默认键位、存档导入导出留到后续。

## 涉及文件

- `src/core/input_service.py`
- `src/scenes/continue_scene.py`
- `config/key_bindings.example.json`
- `docs/sprint_10_save_rename.md`

## 验证情况

- 需要执行语法检查。
- 需要人工验证：
  - 继续游戏页选中存档按 `N` 是否进入重命名。
  - 输入新名称后按 `Enter` 是否保存。
  - 按 `Esc` 是否取消。
  - 改名后关闭游戏再启动，名称是否仍在。

## 下一阶段建议

- Sprint 10 第三小步：把删除、重命名做成可点击按钮，并增加恢复默认键位按钮。
