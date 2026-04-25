# Sprint 10 第一小步：存档名称与删除确认

## 当前阶段

- 当前 Sprint：Sprint 10：存档管理体验优化
- 本次任务：让多存档列表更好识别，并支持安全删除
- 下一阶段建议：Sprint 10 第二小步：手动重命名存档

## 当前阶段目标

- 存档列表不只显示“存档 1/2/3”，要有可读名称。
- 玩家可以删除不需要的存档。
- 删除要有二次确认，避免误删。

## 本阶段完成功能

- 新存档会自动生成名称，例如 `存档 2026-04-26 12:30:00`。
- 旧存档如果没有名称，会自动显示默认名称。
- 继续游戏页存档按钮显示：
  - 序号
  - 存档名称
  - 分数
  - 蛇身长度
  - 更新时间
- 选中存档后按 `Delete`：进入删除确认。
- 再按一次 `Delete`：确认删除该存档。
- 删除确认状态下按 `Esc`：取消删除。
- 删除完成后列表会刷新，并保留合理的选中位置。

## 本阶段页面与 UI 完成情况

继续游戏页 `ContinueScene`：
- 页面标题：`继续游戏`，使用 `TextBlock` 渲染。
- UI 组件：
  - `TextBlock`：标题、滚动提示、底部状态提示。
  - `Button`：每条存档项。
  - `Button`：返回主菜单。
- 存档按钮：
  - 显示自动名称和存档摘要。
  - 点击后读取对应存档。
- 键盘操作：
  - `W/S` 或上下方向键切换存档。
  - `Enter/Space` 读取存档。
  - `Delete` 第一次请求删除。
  - `Delete` 第二次确认删除。
  - `Esc` 在删除确认中取消删除，否则返回主菜单。
- 鼠标操作：
  - 悬停高亮。
  - 点击读取。
  - 滚轮浏览更多存档。
- 状态提示：
  - 底部显示读取/删除相关提示。
  - 删除确认时显示要删除的存档名称。

## 本阶段完成设计

- `SaveSlot` 新增 `name` 字段。
- `SaveService.save()` 创建新存档时生成默认名称。
- `SaveService._parse_slot()` 兼容旧存档：缺少名称时自动生成默认名称。
- `SaveService.rename()` 已预留，用于下一阶段手动重命名。
- `InputService` 增加 `delete_save` 动作，默认键位为 `DELETE`。

## 本阶段数据流设计

- 创建新存档：`GameplayScene._persist_progress()` -> `SaveService.save()` -> 无 `save_id` 时创建 `SaveSlot(name=默认名称)` -> 写入本地 `data/save.json`。
- 展示存档：`ContinueScene.on_enter()` -> `SaveService.list_saves()` -> 渲染带名称的存档按钮。
- 删除存档：`ContinueScene` 选中存档 -> `Delete` -> 记录 `pending_delete_id` -> 再按 `Delete` -> `SaveService.delete(save_id)` -> 更新本地 `data/save.json` -> 刷新列表。

## 本阶段核心业务场景完成进度

- 主菜单业务场景：未变更。
- 设置业务场景：未变更。
- 游戏业务场景：创建新存档时会带默认名称。
- 存档业务场景：完成自动命名、显示名称、安全删除。
- UI 组件化业务场景：继续复用 `Button` 和 `TextBlock`。
- 输入业务场景：新增 `delete_save` 动作。
- 未完成内容：手动重命名、删除按钮、恢复删除均留到后续阶段。

## 涉及文件

- `src/core/system_keys.py`
- `src/core/input_service.py`
- `src/core/save_service.py`
- `src/scenes/continue_scene.py`
- `config/key_bindings.example.json`
- `docs/sprint_10_save_delete_and_names.md`

## 验证情况

- 需要执行语法检查。
- 需要验证 `SaveService` 能兼容旧存档并写入新名称。
- 需要人工验证：
  - 新建存档后继续游戏页显示存档名称。
  - 选中存档后按两次 `Delete` 能删除。
  - 删除确认中按 `Esc` 能取消。

## 下一阶段建议

- Sprint 10 第二小步：支持手动重命名存档。
