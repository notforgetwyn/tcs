from __future__ import annotations

import pygame

from src.constants import BACKGROUND_COLOR, TEXT_COLOR, WINDOW_HEIGHT, WINDOW_WIDTH
from src.core.settings_service import (
    MAX_MOVE_INTERVAL_MS,
    MIN_MOVE_INTERVAL_MS,
    MOVE_INTERVAL_STEP_MS,
    Settings,
)
from src.scenes.base_scene import BaseScene
from src.ui.text import TextBlock


KEY_BINDING_ROWS = [
    ("\u4e0a\u79fb", "move_up"),
    ("\u4e0b\u79fb", "move_down"),
    ("\u5de6\u79fb", "move_left"),
    ("\u53f3\u79fb", "move_right"),
    ("\u4fdd\u5b58\u5e76\u8fd4\u56de\u83dc\u5355", "save_game"),
    ("\u6682\u505c/\u7ee7\u7eed", "pause_game"),
    ("\u6e38\u620f\u7ed3\u675f\u540e\u91cd\u5f00", "restart_game"),
]


class SettingsScene(BaseScene):
    """Allows the player to update speed and key bindings."""

    def __init__(self, app) -> None:
        super().__init__(app)
        loaded = self.app.settings_service.load()
        self.settings = Settings(move_interval_ms=loaded.move_interval_ms)
        self.selected_index = 0
        self.capture_action: str | None = None
        self.status_message = "\u9009\u62e9\u9879\u76ee\u540e\u6309 Enter\uff1b\u9009\u4e2d\u952e\u4f4d\u540e\u518d\u6309\u65b0\u6309\u952e"

    def handle_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._handle_mouse_click(event.pos)
        elif event.type == pygame.MOUSEMOTION:
            self._handle_mouse_motion(event.pos)
        return True

    def on_enter(self) -> None:
        self.app.input_service.sync_many(
            ["debug_toggle", "menu_up", "menu_down", "settings_left", "settings_right", "confirm", "back"]
        )
        self.app.input_service.sync_capture_keys()

    def update(self, delta_ms: int) -> None:
        _ = delta_ms
        if self.capture_action is not None:
            self._update_key_capture()
            return

        if self.app.input_service.just_pressed("debug_toggle"):
            self.app.input_debug.enabled = not self.app.input_debug.enabled
            self.app.input_debug.record_system_key("f3")
        elif self.app.input_service.just_pressed("menu_up"):
            self._move_selection(-1)
            self.app.input_debug.record_system_key("up")
        elif self.app.input_service.just_pressed("menu_down"):
            self._move_selection(1)
            self.app.input_debug.record_system_key("down")
        elif self.selected_index == 0 and self.app.input_service.just_pressed("settings_left"):
            self._adjust_speed(MOVE_INTERVAL_STEP_MS)
            self.app.input_debug.record_system_key("left")
        elif self.selected_index == 0 and self.app.input_service.just_pressed("settings_right"):
            self._adjust_speed(-MOVE_INTERVAL_STEP_MS)
            self.app.input_debug.record_system_key("right")
        elif self.app.input_service.just_pressed("confirm"):
            self.app.input_debug.record_system_key("confirm")
            self._activate_selected()
        elif self.app.input_service.just_pressed("back"):
            self.app.input_debug.record_system_key("escape")
            self.app.change_scene("menu")

    def render(self, screen: pygame.Surface) -> None:
        screen.fill(BACKGROUND_COLOR)
        TextBlock("\u8bbe\u7f6e", 56).draw_center(screen, (WINDOW_WIDTH // 2, 54))
        self._draw_speed_row(screen)
        self._draw_key_binding_rows(screen)
        self._draw_back_row(screen)
        TextBlock(self.status_message, 24).draw_center(screen, (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 34))

        if self.app.input_debug.enabled:
            TextBlock(self.app.input_debug.last_key_text, 20).draw_topleft(screen, (16, WINDOW_HEIGHT - 32))

    def _draw_speed_row(self, screen: pygame.Surface) -> None:
        color = (52, 152, 219) if self.selected_index == 0 else TEXT_COLOR
        prefix = "> " if self.selected_index == 0 else "  "
        suffix = " <" if self.selected_index == 0 else "  "
        text = f"{prefix}\u901f\u5ea6: {self._describe_speed()}  {self.settings.move_interval_ms} ms{suffix}"
        TextBlock(text, 30, color).draw_center(screen, (WINDOW_WIDTH // 2, 112))
        TextBlock("\u9009\u4e2d\u901f\u5ea6\u540e\u6309 A/D \u6216 \u2190/\u2192 \u8c03\u6574\uff0cEnter \u4fdd\u5b58", 20).draw_center(
            screen,
            (WINDOW_WIDTH // 2, 145),
        )

    def _draw_key_binding_rows(self, screen: pygame.Surface) -> None:
        TextBlock("\u952e\u4f4d\u914d\u7f6e\uff08Enter \u5f00\u59cb\u4fee\u6539\uff09", 28).draw_center(
            screen,
            (WINDOW_WIDTH // 2, 188),
        )
        for row_index, (label, action) in enumerate(KEY_BINDING_ROWS, start=1):
            y = self._row_y(row_index)
            color = (52, 152, 219) if self.selected_index == row_index else TEXT_COLOR
            selected = self.selected_index == row_index
            capturing = self.capture_action == action
            marker = "> " if selected else "  "
            tail = " <" if selected else "  "
            key_text = "\u7b49\u5f85\u65b0\u6309\u952e..." if capturing else self.app.input_service.binding_text(action)
            TextBlock(f"{marker}{label}: {key_text}{tail}", 24, color).draw_center(screen, (WINDOW_WIDTH // 2, y))

    def _draw_back_row(self, screen: pygame.Surface) -> None:
        index = self._back_index()
        color = (52, 152, 219) if self.selected_index == index else TEXT_COLOR
        text = "> \u8fd4\u56de\u4e3b\u83dc\u5355 <" if self.selected_index == index else "\u8fd4\u56de\u4e3b\u83dc\u5355"
        TextBlock(text, 30, color).draw_center(screen, (WINDOW_WIDTH // 2, 525))

    def _update_key_capture(self) -> None:
        key_name = self.app.input_service.capture_key_press()
        if key_name is None:
            return

        if key_name == "ESCAPE":
            self.capture_action = None
            self.status_message = "\u5df2\u53d6\u6d88\u952e\u4f4d\u4fee\u6539\u3002"
            self.app.input_service.sync_many(["debug_toggle", "menu_up", "menu_down", "confirm", "back"])
            return

        action = self.capture_action
        conflict = self._configurable_action_using_key(key_name, exclude=action)
        if conflict is not None:
            self.status_message = f"{key_name} \u5df2\u88ab {self._action_label(conflict)} \u4f7f\u7528\uff0c\u8bf7\u6362\u4e00\u4e2a\u952e\u3002"
            self.app.input_service.sync_capture_keys()
            return

        self.app.input_service.set_single_binding(action, key_name)
        self.capture_action = None
        self.status_message = f"\u5df2\u5c06 {self._action_label(action)} \u8bbe\u7f6e\u4e3a {key_name}\uff0c\u7acb\u5373\u751f\u6548\u3002"
        self.app.input_service.sync_many(["debug_toggle", "menu_up", "menu_down", "confirm", "back"])
        self.app.input_service.sync_capture_keys()

    def _activate_selected(self) -> None:
        if self.selected_index == 0:
            self.app.settings_service.save(self.settings)
            self.status_message = "\u8bbe\u7f6e\u5df2\u4fdd\u5b58\u3002"
            return

        key_row = self._key_row_from_index(self.selected_index)
        if key_row is not None:
            label, action = key_row
            self.capture_action = action
            self.status_message = f"\u8bf7\u6309\u65b0\u6309\u952e\u8bbe\u7f6e\u3010{label}\u3011\uff1bEsc \u53d6\u6d88\u3002"
            self.app.input_service.sync_capture_keys()
            return

        self.app.change_scene("menu")

    def _adjust_speed(self, delta: int) -> None:
        next_value = self.settings.move_interval_ms + delta
        self.settings.move_interval_ms = max(
            MIN_MOVE_INTERVAL_MS,
            min(MAX_MOVE_INTERVAL_MS, next_value),
        )
        self.status_message = "\u6309 Enter \u4fdd\u5b58\u8bbe\u7f6e\u3002"

    def _move_selection(self, step: int) -> None:
        self.selected_index = (self.selected_index + step) % (self._back_index() + 1)

    def _build_speed_text(self) -> str:
        return f"\u901f\u5ea6: {self._describe_speed()}\uff08{self.settings.move_interval_ms} \u6beb\u79d2\uff09"

    def _describe_speed(self) -> str:
        interval = self.settings.move_interval_ms
        if interval <= 80:
            return "\u5f88\u5feb"
        if interval <= 120:
            return "\u5feb"
        if interval <= 180:
            return "\u6b63\u5e38"
        if interval <= 220:
            return "\u6162"
        return "\u5f88\u6162"

    def _handle_mouse_click(self, position: tuple[int, int]) -> None:
        selected = self._hit_test(position)
        if selected is None:
            return
        self.selected_index = selected
        self._activate_selected()

    def _handle_mouse_motion(self, position: tuple[int, int]) -> None:
        selected = self._hit_test(position)
        if selected is not None:
            self.selected_index = selected

    def _hit_test(self, position: tuple[int, int]) -> int | None:
        x, y = position
        if not (WINDOW_WIDTH // 2 - 300 <= x <= WINDOW_WIDTH // 2 + 300):
            return None
        if 92 <= y <= 132:
            return 0
        for row_index in range(1, len(KEY_BINDING_ROWS) + 1):
            row_y = self._row_y(row_index)
            if row_y - 16 <= y <= row_y + 16:
                return row_index
        if 502 <= y <= 548:
            return self._back_index()
        return None

    def _row_y(self, row_index: int) -> int:
        return 220 + (row_index - 1) * 36

    def _back_index(self) -> int:
        return len(KEY_BINDING_ROWS) + 1

    def _key_row_from_index(self, index: int) -> tuple[str, str] | None:
        if 1 <= index <= len(KEY_BINDING_ROWS):
            return KEY_BINDING_ROWS[index - 1]
        return None

    def _action_label(self, action: str) -> str:
        for label, row_action in KEY_BINDING_ROWS:
            if row_action == action:
                return label
        return action

    def _configurable_action_using_key(self, key_name: str, *, exclude: str) -> str | None:
        for _, action in KEY_BINDING_ROWS:
            if action != exclude and key_name in self.app.input_service.bindings.get(action, []):
                return action
        return None
