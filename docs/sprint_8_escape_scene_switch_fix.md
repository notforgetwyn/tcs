# Sprint 8 补充：ESC 返回菜单误退出修复

## 当前阶段

- 当前 Sprint：Sprint 8：UI 组件深化
- 本次补充任务：修复游戏中按 `Esc` 返回菜单后程序直接退出的问题
- 下一阶段建议：Sprint 9：输入服务抽象与可配置键位

## 问题说明

用户期望：

- 游戏中按 `Esc` 应保存进度并返回主菜单。
- 返回主菜单后程序不应退出。

实际现象：

- 游戏中按 `Esc` 后，程序直接结束。

## 根因

项目当前使用 Windows 系统级按键状态模拟 KEYDOWN。

游戏页处理 `Esc` 的流程是：

```text
GameplayScene.update()
  -> 检测到 Esc just_pressed
  -> 保存进度
  -> App.change_scene("menu")
```

但切到菜单页后，物理 `Esc` 按键通常还没有松开。菜单页下一帧会继续读取到：

```text
MenuScene.update()
  -> 检测到 Esc just_pressed
  -> App.stop()
```

所以同一次按键穿透到了下一个场景，导致“返回菜单”变成“退出游戏”。

## 修复方案

- 为场景增加 `on_enter()` 生命周期钩子。
- 在场景切换完成后调用 `scene.on_enter()`。
- `on_enter()` 中同步当前系统按键状态，把正在按住的键记录为已处理。
- 用户必须松开再重新按下，才会触发新场景的 KEYDOWN 动作。

## 修复后的数据流

```text
游戏中按 Esc
  -> GameplayScene 检测 Esc
  -> 保存进度
  -> App.change_scene("menu")
  -> MenuScene.on_enter()
  -> sync 当前 Esc 状态为已按下
  -> 菜单页不会把同一次 Esc 当成退出
```

## 本次涉及文件

- `src/core/system_keys.py`
- `src/scenes/base_scene.py`
- `src/scenes/menu_scene.py`
- `src/scenes/continue_scene.py`
- `src/scenes/settings_scene.py`
- `src/scenes/gameplay_scene.py`
- `src/app.py`
- `data/save.json`
- `docs/sprint_8_escape_scene_switch_fix.md`

## 验证要点

- 游戏中按 `Esc`：应返回主菜单，不退出程序。
- 回到菜单后松开 `Esc`，再按一次 `Esc`：才退出程序。
- 主菜单、设置页、继续游戏页的键盘操作仍应正常。
