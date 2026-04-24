# Sprint 8：UI 组件深化

## 当前阶段

- 当前 Sprint：Sprint 8：UI 组件深化
- 上一阶段：Sprint 7：工程优化第二小步
- 下一阶段建议：Sprint 9：输入服务抽象与可配置键位

## 当前阶段目标

- 继续把 UI 逻辑从页面中抽离出来。
- 优化按钮组件的视觉状态，让键盘选择、鼠标悬停、禁用状态更清晰。
- 让继续游戏页的按钮交互更接近真实客户端页面。
- 更新 README，保证启动方式、输入方式和当前项目状态清晰可读。

## 本阶段完成功能

- `Button` 组件新增 hover 状态。
- `Button` 组件新增统一边框颜色和不同状态的边框宽度。
- `ContinueScene` 支持鼠标悬停按钮时自动同步当前选中按钮。
- `ContinueScene` 按钮渲染区分 selected 与 hovered 状态。
- README 已重写为正常中文，补充当前 Sprint、启动命令、输入系统说明和文档索引。
- 恢复 `data/save.json` 为空存档状态，避免测试运行数据进入提交。

## 本阶段页面与 UI 设计

### 主菜单页面

- 页面：`MenuScene`
- 当前 UI：`MenuList`
- 本阶段状态：保持现有菜单文本式 UI，不做大改。
- 原因：主菜单后续会整体切换为按钮式菜单，本阶段只先深化已有按钮组件，避免一次改动过大。

### 继续游戏页面

- 页面：`ContinueScene`
- 当前 UI：`Button`
- 本阶段完成：
  - `继续游戏` 按钮可键盘选中。
  - `返回主菜单` 按钮可键盘选中。
  - 鼠标移动到按钮上时，按钮进入 hover 状态。
  - 鼠标 hover 的按钮会同步成为当前 selected 按钮。
  - 鼠标左键点击按钮会立即执行对应操作。
- 点击结果：
  - 点击 `继续游戏`：存在存档时进入游戏并恢复状态。
  - 点击 `返回主菜单`：返回主菜单。
- 数据结果：
  - 继续游戏页从 `SaveService.load()` 读取 `data/save.json`。
  - 页面只展示存档摘要，不直接修改存档。

### 设置页面

- 页面：`SettingsScene`
- 当前 UI：文本式选项。
- 本阶段状态：保持现有交互。
- 后续计划：迁移到通用按钮/滑块组件，让速度调整更直观。

### 游戏页面

- 页面：`GameplayScene`
- 当前 UI：网格、蛇、食物、HUD、结束提示。
- 本阶段状态：保持玩法 UI 不变。
- 后续计划：增加暂停面板、游戏结束按钮、分数面板样式。

## 本阶段组件设计

### Button

- 文件：`src/ui/button.py`
- 新增状态：
  - `normal`：普通状态。
  - `hovered`：鼠标悬停状态。
  - `selected`：键盘或鼠标当前选中状态。
  - `disabled`：不可点击状态。
- 新增能力：
  - 统一圆角半径。
  - 统一边框颜色。
  - selected 状态边框更粗。
  - hovered 状态使用独立颜色。

### UI 常量

- 文件：`src/constants.py`
- 新增常量：
  - `PANEL_COLOR`
  - `BUTTON_NORMAL_COLOR`
  - `BUTTON_ACTIVE_COLOR`
  - `BUTTON_HOVER_COLOR`
  - `BUTTON_DISABLED_COLOR`
  - `BUTTON_BORDER_COLOR`
- 设计目的：
  - 避免 UI 组件内部散落硬编码颜色。
  - 后续可以统一调整整体视觉风格。

## 本阶段数据流设计

```text
鼠标移动
  -> Pygame MOUSEMOTION
  -> ContinueScene._handle_mouse_motion()
  -> Button.contains()
  -> hovered_index / selected_index
  -> Button.draw(selected, hovered)
  -> 屏幕显示 hover/selected 状态
```

```text
鼠标点击
  -> Pygame MOUSEBUTTONDOWN
  -> ContinueScene._handle_mouse_click()
  -> Button.contains()
  -> selected_index
  -> _activate_selected()
  -> 继续游戏 / 返回主菜单
```

```text
键盘输入
  -> Windows GetAsyncKeyState
  -> KeyEdges.just_pressed()
  -> ContinueScene.update()
  -> selected_index
  -> Button.draw(selected=True)
```

## 本阶段涉及文件

- `src/constants.py`
- `src/ui/button.py`
- `src/scenes/continue_scene.py`
- `README.md`
- `docs/sprint_8_ui_components.md`
- `data/save.json`

## 验证计划

- 运行语法检查：

```powershell
& 'D:\ananconda\python.exe' -m compileall main.py src tools
```

- 启动游戏后人工验证：
  - 主菜单进入继续游戏页。
  - 鼠标悬停按钮时按钮高亮。
  - 鼠标点击按钮能触发动作。
  - 键盘 `W/S` 仍能切换按钮。
  - `Enter` / `Space` 仍能确认按钮。

## 下一阶段建议

- 进入 Sprint 9：输入服务抽象与可配置键位。
- 将 `system_keys.py` 和 `input_keys.py` 进一步收敛为 `InputService`。
- 将键位映射保存到 JSON 配置。
- 设置页增加键位配置入口。
