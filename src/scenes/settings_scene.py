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
from src.ui.menu_list import MenuList
from src.ui.text import TextBlock


class SettingsScene(BaseScene):
    """Allows the player to update movement speed and save it."""

    def __init__(self, app) -> None:
        super().__init__(app)
        loaded = self.app.settings_service.load()
        self.settings = Settings(move_interval_ms=loaded.move_interval_ms)
        self.menu_list = MenuList(
            ["\u901f\u5ea6", "\u8fd4\u56de\u4e3b\u83dc\u5355"],
            font_size=36,
            spacing=80,
        )
        self.status_message = "\u5de6\u53f3\u952e\u8c03\u6574\u901f\u5ea6\uff0cEnter \u4fdd\u5b58"

    def handle_event(self, event: pygame.event.Event) -> bool:
        if event.type != pygame.KEYDOWN:
            return True

        if self._is_up_input(event):
            self.menu_list.move_up()
        elif self._is_down_input(event):
            self.menu_list.move_down()
        elif self.menu_list.selected_index == 0 and self._is_left_input(event):
            self._adjust_speed(MOVE_INTERVAL_STEP_MS)
        elif self.menu_list.selected_index == 0 and self._is_right_input(event):
            self._adjust_speed(-MOVE_INTERVAL_STEP_MS)
        elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
            if self.menu_list.selected_index == 0:
                self.app.settings_service.save(self.settings)
                self.status_message = "\u8bbe\u7f6e\u5df2\u4fdd\u5b58\u3002"
            else:
                self.app.change_scene("menu")
        elif event.key == pygame.K_ESCAPE:
            self.app.change_scene("menu")

        return True

    def render(self, screen: pygame.Surface) -> None:
        screen.fill(BACKGROUND_COLOR)
        TextBlock("\u8bbe\u7f6e", 64).draw_center(screen, (WINDOW_WIDTH // 2, 120))

        speed_color = (52, 152, 219) if self.menu_list.selected_index == 0 else TEXT_COLOR
        TextBlock(self._build_speed_text(), 36, speed_color).draw_center(
            screen,
            (WINDOW_WIDTH // 2, 260),
        )

        back_color = (52, 152, 219) if self.menu_list.selected_index == 1 else TEXT_COLOR
        TextBlock("\u8fd4\u56de\u4e3b\u83dc\u5355", 36, back_color).draw_center(
            screen,
            (WINDOW_WIDTH // 2, 340),
        )
        TextBlock(self.status_message, 28).draw_center(screen, (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 90))

    def _adjust_speed(self, delta: int) -> None:
        next_value = self.settings.move_interval_ms + delta
        self.settings.move_interval_ms = max(
            MIN_MOVE_INTERVAL_MS,
            min(MAX_MOVE_INTERVAL_MS, next_value),
        )
        self.status_message = "\u6309 Enter \u4fdd\u5b58\u8bbe\u7f6e\u3002"

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

    def _is_up_input(self, event: pygame.event.Event) -> bool:
        return event.key in (pygame.K_UP, pygame.K_w) or getattr(event, "unicode", "").lower() == "w"

    def _is_down_input(self, event: pygame.event.Event) -> bool:
        return event.key in (pygame.K_DOWN, pygame.K_s) or getattr(event, "unicode", "").lower() == "s"

    def _is_left_input(self, event: pygame.event.Event) -> bool:
        return event.key in (pygame.K_LEFT, pygame.K_a) or getattr(event, "unicode", "").lower() == "a"

    def _is_right_input(self, event: pygame.event.Event) -> bool:
        return event.key in (pygame.K_RIGHT, pygame.K_d) or getattr(event, "unicode", "").lower() == "d"
