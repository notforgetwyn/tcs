from __future__ import annotations

import pygame

from src.constants import BACKGROUND_COLOR, TEXT_COLOR, WINDOW_HEIGHT, WINDOW_WIDTH
from src.core.settings_service import (
    MAX_MOVE_INTERVAL_MS,
    MIN_MOVE_INTERVAL_MS,
    MOVE_INTERVAL_STEP_MS,
    Settings,
)
from src.ui.font_manager import get_font


class SettingsScene:
    """Allows the player to update movement speed and save it."""

    def __init__(self, app) -> None:
        self.app = app
        self.title_font = get_font(64)
        self.body_font = get_font(36)
        self.small_font = get_font(28)
        loaded = self.app.settings_service.load()
        self.settings = Settings(move_interval_ms=loaded.move_interval_ms)
        self.selected_index = 0
        self.status_message = "左右键调整速度，Enter 保存"

    def handle_event(self, event: pygame.event.Event) -> bool:
        if event.type != pygame.KEYDOWN:
            return True

        if event.key in (pygame.K_UP, pygame.K_w):
            self.selected_index = (self.selected_index - 1) % 2
        elif event.key in (pygame.K_DOWN, pygame.K_s):
            self.selected_index = (self.selected_index + 1) % 2
        elif event.key in (pygame.K_LEFT, pygame.K_a) and self.selected_index == 0:
            self._adjust_speed(MOVE_INTERVAL_STEP_MS)
        elif event.key in (pygame.K_RIGHT, pygame.K_d) and self.selected_index == 0:
            self._adjust_speed(-MOVE_INTERVAL_STEP_MS)
        elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
            if self.selected_index == 0:
                self.app.settings_service.save(self.settings)
                self.status_message = "设置已保存。"
            else:
                self.app.change_scene("menu")
        elif event.key == pygame.K_ESCAPE:
            self.app.change_scene("menu")

        return True

    def update(self, delta_ms: int) -> None:
        _ = delta_ms

    def render(self, screen: pygame.Surface) -> None:
        screen.fill(BACKGROUND_COLOR)

        title_surface = self.title_font.render("设置", True, TEXT_COLOR)
        title_rect = title_surface.get_rect(center=(WINDOW_WIDTH // 2, 120))
        screen.blit(title_surface, title_rect)

        speed_text = self._build_speed_text()
        speed_color = (52, 152, 219) if self.selected_index == 0 else TEXT_COLOR
        speed_surface = self.body_font.render(speed_text, True, speed_color)
        speed_rect = speed_surface.get_rect(center=(WINDOW_WIDTH // 2, 260))
        screen.blit(speed_surface, speed_rect)

        back_color = (52, 152, 219) if self.selected_index == 1 else TEXT_COLOR
        back_surface = self.body_font.render("返回主菜单", True, back_color)
        back_rect = back_surface.get_rect(center=(WINDOW_WIDTH // 2, 340))
        screen.blit(back_surface, back_rect)

        hint_surface = self.small_font.render(self.status_message, True, TEXT_COLOR)
        hint_rect = hint_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 90))
        screen.blit(hint_surface, hint_rect)

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
