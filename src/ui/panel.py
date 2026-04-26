from __future__ import annotations

import pygame

from src.constants import BUTTON_BORDER_COLOR, PANEL_COLOR


class Panel:
    """Reusable rounded container for grouped UI content."""

    def __init__(
        self,
        rect: pygame.Rect,
        *,
        fill_color: tuple[int, int, int] = PANEL_COLOR,
        border_color: tuple[int, int, int] = BUTTON_BORDER_COLOR,
        border_width: int = 2,
        border_radius: int = 10,
    ) -> None:
        self.rect = rect
        self.fill_color = fill_color
        self.border_color = border_color
        self.border_width = border_width
        self.border_radius = border_radius

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(screen, self.fill_color, self.rect, border_radius=self.border_radius)
        pygame.draw.rect(
            screen,
            self.border_color,
            self.rect,
            width=self.border_width,
            border_radius=self.border_radius,
        )
