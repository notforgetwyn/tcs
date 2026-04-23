from __future__ import annotations

import pygame

from src.constants import BACKGROUND_COLOR, TEXT_COLOR, WINDOW_HEIGHT, WINDOW_WIDTH


class MenuScene:
    """Main menu scene used as the application's entry point."""

    def __init__(self, app) -> None:
        self.app = app
        self.title_font = pygame.font.SysFont(None, 72)
        self.item_font = pygame.font.SysFont(None, 42)
        self.hint_font = pygame.font.SysFont(None, 28)
        self.options = [
            ("开始游戏", "gameplay"),
            ("继续游戏", "continue_unavailable"),
            ("设置", "settings"),
            ("退出游戏", "exit"),
        ]
        self.selected_index = 0

    def handle_event(self, event: pygame.event.Event) -> bool:
        if event.type != pygame.KEYDOWN:
            return True

        if event.key in (pygame.K_UP, pygame.K_w):
            self.selected_index = (self.selected_index - 1) % len(self.options)
        elif event.key in (pygame.K_DOWN, pygame.K_s):
            self.selected_index = (self.selected_index + 1) % len(self.options)
        elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
            self._activate_selected()
        elif event.key == pygame.K_ESCAPE:
            return False

        return True

    def update(self, delta_ms: int) -> None:
        _ = delta_ms

    def render(self, screen: pygame.Surface) -> None:
        screen.fill(BACKGROUND_COLOR)

        title_surface = self.title_font.render("贪吃蛇", True, TEXT_COLOR)
        title_rect = title_surface.get_rect(center=(WINDOW_WIDTH // 2, 120))
        screen.blit(title_surface, title_rect)

        for index, (label, _) in enumerate(self.options):
            is_selected = index == self.selected_index
            color = (52, 152, 219) if is_selected else TEXT_COLOR
            item_surface = self.item_font.render(label, True, color)
            item_rect = item_surface.get_rect(center=(WINDOW_WIDTH // 2, 240 + index * 70))
            screen.blit(item_surface, item_rect)

        hint_surface = self.hint_font.render(
            "使用 W/S 或 方向键选择，按 Enter 确认",
            True,
            TEXT_COLOR,
        )
        hint_rect = hint_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 70))
        screen.blit(hint_surface, hint_rect)

    def _activate_selected(self) -> None:
        _, action = self.options[self.selected_index]
        if action == "exit":
            self.app.stop()
            return
        self.app.change_scene(action)
