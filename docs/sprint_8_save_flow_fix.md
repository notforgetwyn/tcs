# Sprint 8 补充：存档流程语义修复

## 当前阶段

- 当前 Sprint：Sprint 8：UI 组件深化
- 本次补充任务：修复启动程序时误创建存档的问题
- 下一阶段建议：Sprint 9：输入服务抽象与可配置键位

## 问题说明

用户要求：

- `开始游戏` 表示开启一个新的存档。
- `继续游戏` 表示读取已有存档。
- 没有开始过游戏时，不应该自动生成可继续的存档。

实际问题：

- 程序启动时，`App.__init__` 提前创建了 `GameplayScene(self)`。
- `GameplayScene` 在新游戏构造时会调用 `_persist_progress()`。
- 因此即使用户还没有点击 `开始游戏`，`data/save.json` 也会被写入 `has_save: true`。

## 根因

```text
程序启动
  -> App.__init__()
  -> self.scenes 中提前创建 GameplayScene(self)
  -> GameplayScene.__init__(game_state=None)
  -> 创建蛇、食物、初始分数
  -> _persist_progress()
  -> data/save.json 变成 has_save: true
```

这个流程把“预加载游戏页”和“开始新游戏”混在了一起，导致启动程序就产生新存档。

## 修复方案

- `App.__init__` 不再提前创建 `GameplayScene`。
- 只有以下入口会创建 `GameplayScene`：
  - `start_new_game()`：开始一个全新的游戏，并创建新存档。
  - `load_gameplay_from_state()`：从已有 `GameState` 恢复游戏。
  - `change_scene("gameplay")`：保留兼容入口，但当前主菜单使用 `start_new_game()`。

## 修复后的数据流

### 启动程序

```text
App.__init__()
  -> 创建 MenuScene / SettingsScene / ContinueScene
  -> 不创建 GameplayScene
  -> 不写入 data/save.json
```

### 点击开始游戏

```text
MenuScene._activate_selected()
  -> App.start_new_game()
  -> SaveService.clear()
  -> GameplayScene(game_state=None)
  -> 生成初始蛇和食物
  -> _persist_progress()
  -> data/save.json 写入新游戏存档
```

### 点击继续游戏

```text
MenuScene._activate_selected()
  -> App.change_scene("continue_game")
  -> ContinueScene
  -> SaveService.load()
  -> 有存档：展示继续游戏按钮
  -> 无存档：展示无存档提示
```

## 本次涉及文件

- `src/app.py`
- `data/save.json`
- `docs/sprint_8_save_flow_fix.md`

## 验证要点

- 刚启动程序，不应该因为进入主菜单就自动创建新存档。
- 点击 `继续游戏`，无存档时应显示无存档提示。
- 点击 `开始游戏`，应创建一个新的 `data/save.json` 存档。
- 游戏中返回主菜单后，再点击 `继续游戏`，应能读取刚才的存档。
