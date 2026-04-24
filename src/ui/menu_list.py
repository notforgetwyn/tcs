from __future__ import annotations

import pygame

from src.constants import TEXT_COLOR
from src.ui.font_manager import get_font


class MenuList:
    """Renders a vertical menu and tracks selection."""

    def __init__(
        self,
        items: list[str],
        *,
        font_size: int = 42,
        normal_color: tuple[int, int, int] = TEXT_COLOR,
        active_color: tuple[int, int, int] = (52, 152, 219),
        spacing: int = 70,
    ) -> None:
        self.items = items
        self.font = get_font(font_size)
        self.normal_color = normal_color
        self.active_color = active_color
        self.spacing = spacing
        self.selected_index = 0

    def move_up(self) -> None:
        self.selected_index = (self.selected_index - 1) % len(self.items)

    def move_down(self) -> None:
        self.selected_index = (self.selected_index + 1) % len(self.items)

    def draw_centered(self, screen: pygame.Surface, center_x: int, start_y: int) -> None:
        for index, label in enumerate(self.items):
            is_active = index == self.selected_index
            color = self.active_color if is_active else self.normal_color
            text = f"> {label} <" if is_active else label
            surface = self.font.render(text, True, color)
            rect = surface.get_rect(center=(center_x, start_y + index * self.spacing))
            screen.blit(surface, rect)
