from __future__ import annotations

import pygame

from src.constants import (
    BUTTON_ACTIVE_COLOR,
    BUTTON_BORDER_COLOR,
    BUTTON_DISABLED_COLOR,
    BUTTON_HOVER_COLOR,
    BUTTON_NORMAL_COLOR,
    TEXT_COLOR,
)
from src.ui.font_manager import get_font


class Button:
    """Keyboard-selectable and mouse-clickable button."""

    def __init__(
        self,
        text: str,
        rect: pygame.Rect,
        *,
        font_size: int = 32,
        normal_color: tuple[int, int, int] = BUTTON_NORMAL_COLOR,
        active_color: tuple[int, int, int] = BUTTON_ACTIVE_COLOR,
        hover_color: tuple[int, int, int] = BUTTON_HOVER_COLOR,
        disabled_color: tuple[int, int, int] = BUTTON_DISABLED_COLOR,
        border_color: tuple[int, int, int] = BUTTON_BORDER_COLOR,
        text_color: tuple[int, int, int] = TEXT_COLOR,
        enabled: bool = True,
    ) -> None:
        self.text = text
        self.rect = rect
        self.font = get_font(font_size)
        self.normal_color = normal_color
        self.active_color = active_color
        self.hover_color = hover_color
        self.disabled_color = disabled_color
        self.border_color = border_color
        self.text_color = text_color
        self.enabled = enabled

    def draw(self, screen: pygame.Surface, *, selected: bool = False, hovered: bool = False) -> None:
        if not self.enabled:
            color = self.disabled_color
            border_width = 1
        elif selected:
            color = self.active_color
            border_width = 3
        elif hovered:
            color = self.hover_color
            border_width = 2
        else:
            color = self.normal_color
            border_width = 1

        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, self.border_color, self.rect, width=border_width, border_radius=10)
        surface = self.font.render(self.text, True, self.text_color)
        text_rect = surface.get_rect(center=self.rect.center)
        screen.blit(surface, text_rect)

    def contains(self, position: tuple[int, int]) -> bool:
        return self.enabled and self.rect.collidepoint(position)
