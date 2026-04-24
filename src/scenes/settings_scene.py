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
        self.menu_list = MenuList(["速度", "返回主菜单"], font_size=36, spacing=80)
        self.status_message = "左右键调整速度，Enter 保存"

    def handle_event(self, event: pygame.event.Event) -> bool:
        if event.type != pygame.KEYDOWN:
            return True

        if event.key in (pygame.K_UP, pygame.K_w):
            self.menu_list.move_up()
        elif event.key in (pygame.K_DOWN, pygame.K_s):
            self.menu_list.move_down()
        elif event.key in (pygame.K_LEFT, pygame.K_a) and self.menu_list.selected_index == 0:
            self._adjust_speed(MOVE_INTERVAL_STEP_MS)
        elif event.key in (pygame.K_RIGHT, pygame.K_d) and self.menu_list.selected_index == 0:
            self._adjust_speed(-MOVE_INTERVAL_STEP_MS)
        elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
            if self.menu_list.selected_index == 0:
                self.app.settings_service.save(self.settings)
                self.status_message = "设置已保存。"
            else:
                self.app.change_scene("menu")
        elif event.key == pygame.K_ESCAPE:
            self.app.change_scene("menu")

        return True

    def render(self, screen: pygame.Surface) -> None:
        screen.fill(BACKGROUND_COLOR)
        TextBlock("设置", 64).draw_center(screen, (WINDOW_WIDTH // 2, 120))

        speed_color = (52, 152, 219) if self.menu_list.selected_index == 0 else TEXT_COLOR
        TextBlock(self._build_speed_text(), 36, speed_color).draw_center(
            screen,
            (WINDOW_WIDTH // 2, 260),
        )

        back_color = (52, 152, 219) if self.menu_list.selected_index == 1 else TEXT_COLOR
        TextBlock("返回主菜单", 36, back_color).draw_center(screen, (WINDOW_WIDTH // 2, 340))
        TextBlock(self.status_message, 28).draw_center(screen, (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 90))

    def _adjust_speed(self, delta: int) -> None:
        next_value = self.settings.move_interval_ms + delta
        self.settings.move_interval_ms = max(
            MIN_MOVE_INTERVAL_MS,
            min(MAX_MOVE_INTERVAL_MS, next_value),
        )
        self.status_message = "按 Enter 保存设置。"

    def _build_speed_text(self) -> str:
        return f"速度: {self._describe_speed()}（{self.settings.move_interval_ms} 毫秒）"

    def _describe_speed(self) -> str:
        interval = self.settings.move_interval_ms
        if interval <= 80:
            return "很快"
        if interval <= 120:
            return "快"
        if interval <= 180:
            return "正常"
        if interval <= 220:
            return "慢"
        return "很慢"
