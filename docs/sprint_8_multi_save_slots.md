# Sprint 8 补充：多存档列表与保存后返回菜单

## 当前阶段

- 当前 Sprint：Sprint 8：UI 组件深化
- 本次补充任务：将单存档升级为多存档，并调整游戏内保存行为
- 下一阶段建议：Sprint 9：输入服务抽象与可配置键位

## 当前阶段目标

- 游戏中按 `E` 保存后应结束当前游戏流程并返回主菜单。
- `继续游戏` 页面不能只显示一个存档，应显示多个可读取存档。
- `开始游戏` 应创建一个新的存档槽，不应该覆盖旧存档。

## 本阶段完成功能

- `data/save.json` 从单存档结构升级为多存档列表结构。
- 点击 `开始游戏`：创建一个新的游戏存档槽。
- 游戏过程中自动保存：只更新当前游戏对应的存档槽。
- 游戏中按 `E`：保存当前存档，并返回主菜单。
- 点击 `继续游戏`：进入多存档选择页。
- 继续游戏页可以显示多个存档。
- 每个存档按钮显示：
  - 存档序号
  - 当前分数
  - 蛇身长度
  - 最后更新时间
- 支持键盘 `W/S` 或方向键选择不同存档。
- 支持鼠标悬停高亮和点击读取存档。
- 如果存档超过 5 个，键盘选择时会自动滚动可见列表。

## 本阶段完成设计

### 存档数据设计

旧结构：

```json
{
  "has_save": true,
  "game_state": {}
}
```

新结构：

```json
{
  "saves": [
    {
      "id": "唯一存档ID",
      "created_at": "创建时间",
      "updated_at": "更新时间",
      "game_state": {}
    }
  ]
}
```

### SaveService

- 文件：`src/core/save_service.py`
- 新增 `SaveSlot` 数据结构。
- 新增 `list_saves()`：读取所有有效存档。
- `save(game_state, save_id)`：
  - 有 `save_id` 时更新已有存档槽。
  - 无 `save_id` 时创建新存档槽。
- `load(save_id)`：读取指定存档。
- `delete(save_id)`：删除指定存档。
- 保留旧单存档格式迁移能力。

### 游戏页面

- 页面：`GameplayScene`
- 新增 `save_id` 字段，记录当前游戏绑定的存档槽。
- 自动保存只更新当前 `save_id`。
- 按 `E`：
  - 保存当前状态。
  - 返回主菜单。
- 游戏结束：
  - 删除当前存档槽。

### 继续游戏页面

- 页面：`ContinueScene`
- UI 组件：`Button`
- 页面 UI：
  - 多个存档按钮。
  - 返回主菜单按钮。
- 存档按钮能不能点：
  - 有效存档按钮可以点击。
  - 点击后读取对应存档进入游戏。
- 返回按钮能不能点：
  - 可以点击。
  - 点击后返回主菜单。

## 数据流设计

### 开始新游戏

```text
主菜单点击开始游戏
  -> App.start_new_game()
  -> GameplayScene(game_state=None, save_id=None)
  -> GameplayScene._persist_progress()
  -> SaveService.save(game_state, save_id=None)
  -> 创建新 SaveSlot
  -> data/save.json
```

### 游戏中自动保存

```text
蛇移动后
  -> GameplayScene._persist_progress()
  -> SaveService.save(game_state, save_id=当前存档ID)
  -> 更新当前 SaveSlot
```

### 游戏中按 E 保存

```text
按 E
  -> GameplayScene._persist_progress()
  -> App.change_scene("menu")
  -> 回到主菜单
```

### 继续游戏读取多存档

```text
主菜单点击继续游戏
  -> ContinueScene
  -> SaveService.list_saves()
  -> 渲染多个存档按钮
  -> 点击某个存档
  -> App.load_gameplay_from_state(game_state, save_id)
  -> GameplayScene 继续更新同一个存档槽
```

## 涉及文件

- `src/core/save_service.py`
- `src/scenes/gameplay_scene.py`
- `src/scenes/continue_scene.py`
- `src/app.py`
- `data/save.json`
- `docs/sprint_8_multi_save_slots.md`

## 验证情况

- 需要执行语法检查。
- 需要人工验证：
  - 开始游戏后生成一个新存档。
  - 游戏中按 `E` 后返回主菜单。
  - 多次开始游戏并保存后，继续游戏页能看到多个存档。
  - 点击不同存档能进入对应游戏状态。

## 下一阶段建议

- 进入 Sprint 9：输入服务抽象与可配置键位。
- 后续可以继续增加存档删除、存档命名、存档时间格式优化。
