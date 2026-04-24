from __future__ import annotations

import pygame

from src.constants import BACKGROUND_COLOR, WINDOW_HEIGHT, WINDOW_WIDTH
from src.scenes.base_scene import BaseScene
from src.ui.text import TextBlock


class PlaceholderScene(BaseScene):
    """Temporary scene for features scheduled in later iterations."""

    def __init__(self, app, title: str, message: str) -> None:
        super().__init__(app)
        self.title = title
        self.message = message

    def handle_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_RETURN):
            self.app.change_scene("menu")
        return True

    def render(self, screen: pygame.Surface) -> None:
        screen.fill(BACKGROUND_COLOR)
        center_x = WINDOW_WIDTH // 2
        center_y = WINDOW_HEIGHT // 2
        TextBlock(self.title, 64).draw_center(screen, (center_x, center_y - 70))
        TextBlock(self.message, 32).draw_center(screen, (center_x, center_y))
        TextBlock("按 Enter 或 ESC 返回", 32).draw_center(screen, (center_x, center_y + 60))
