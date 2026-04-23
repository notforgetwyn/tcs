from __future__ import annotations

import pygame

from src.constants import BACKGROUND_COLOR, TEXT_COLOR, WINDOW_HEIGHT, WINDOW_WIDTH


class PlaceholderScene:
    """Temporary scene for features scheduled in later iterations."""

    def __init__(self, app, title: str, message: str) -> None:
        self.app = app
        self.title = title
        self.message = message
        self.title_font = pygame.font.SysFont(None, 64)
        self.body_font = pygame.font.SysFont(None, 32)

    def handle_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_RETURN):
            self.app.change_scene("menu")
        return True

    def update(self, delta_ms: int) -> None:
        _ = delta_ms

    def render(self, screen: pygame.Surface) -> None:
        screen.fill(BACKGROUND_COLOR)

        title_surface = self.title_font.render(self.title, True, TEXT_COLOR)
        message_surface = self.body_font.render(self.message, True, TEXT_COLOR)
        hint_surface = self.body_font.render("按 Enter 或 ESC 返回", True, TEXT_COLOR)

        title_rect = title_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 70))
        message_rect = message_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        hint_rect = hint_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 60))

        screen.blit(title_surface, title_rect)
        screen.blit(message_surface, message_rect)
        screen.blit(hint_surface, hint_rect)
