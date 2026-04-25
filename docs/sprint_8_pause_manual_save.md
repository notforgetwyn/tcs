# Sprint 8 补充：游戏内暂停与手动保存

## 当前阶段

- 当前 Sprint：Sprint 8：UI 组件深化
- 本次补充任务：游戏中新增 `E` 手动保存和 `P` 暂停/继续
- 下一阶段建议：Sprint 9：输入服务抽象与可配置键位

## 当前阶段目标

- 让玩家在游戏中可以主动保存当前进度。
- 让玩家可以暂停游戏，暂停期间蛇不继续移动。
- 保持现有自动保存、继续游戏、返回菜单逻辑不受影响。

## 本阶段完成功能

- 游戏中按 `E`：立即保存当前存档。
- 游戏中按 `P`：切换暂停/继续。
- 暂停期间：
  - 蛇不移动。
  - 不处理方向移动。
  - 不执行移动后的自动保存。
  - 仍允许按 `E` 保存当前状态。
  - 仍允许按 `Esc` 保存并返回主菜单。
- 游戏 HUD 增加操作提示：
  - `保存: E`
  - `暂停: P`
- 暂停时显示半透明遮罩和中文暂停提示。

## 本阶段完成设计

### 游戏页面

- 页面：`GameplayScene`
- 新增 UI：
  - 暂停遮罩。
  - 暂停标题：`游戏暂停`。
  - 暂停操作提示：`按 P 继续，按 E 保存，按 ESC 返回主菜单`。
  - 状态提示：保存成功、已暂停、已继续游戏。
- 新增按键：
  - `E`：手动保存。
  - `P`：暂停/继续。
- 按钮/组件说明：
  - 当前游戏页没有鼠标按钮。
  - 暂停与保存通过键盘触发。

### 输入数据流

```text
Windows 物理键盘
  -> system_keys.GetAsyncKeyState
  -> KeyEdges.just_pressed("save", VK_E)
  -> GameplayScene._persist_progress()
  -> SaveService.save()
  -> data/save.json
```

```text
Windows 物理键盘
  -> system_keys.GetAsyncKeyState
  -> KeyEdges.just_pressed("pause", VK_P)
  -> GameplayScene.is_paused = True/False
  -> 暂停时跳过蛇移动与碰撞更新
  -> render() 绘制暂停遮罩
```

### 核心业务边界

- 本阶段只做游戏内暂停与手动保存。
- 暂停状态暂不写入存档，读取存档后默认继续游戏。
- 暂不做暂停菜单按钮，后续 UI 组件深化时再加。

## 涉及文件

- `src/core/system_keys.py`
- `src/scenes/gameplay_scene.py`
- `data/save.json`
- `docs/sprint_8_pause_manual_save.md`

## 验证情况

- 需要执行语法检查。
- 需要人工验证：
  - 游戏中按 `E` 后返回菜单，再继续游戏可读取当前进度。
  - 游戏中按 `P` 后蛇停止移动。
  - 再按 `P` 后继续移动。
  - 暂停时按 `Esc` 返回菜单，不退出程序。

## 下一阶段建议

- 进入 Sprint 9：输入服务抽象与可配置键位。
- 将 `E`、`P`、`Esc`、方向键统一纳入可配置键位表。
