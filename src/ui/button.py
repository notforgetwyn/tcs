from __future__ import annotations

import pygame

from src.constants import BACKGROUND_COLOR, TEXT_COLOR
from src.ui.font_manager import get_font


class Button:
    """Keyboard-selectable and mouse-clickable button."""

    def __init__(
        self,
        text: str,
        rect: pygame.Rect,
        *,
        font_size: int = 32,
        normal_color: tuple[int, int, int] = (44, 62, 80),
        active_color: tuple[int, int, int] = (52, 152, 219),
        disabled_color: tuple[int, int, int] = (90, 90, 90),
        text_color: tuple[int, int, int] = TEXT_COLOR,
        enabled: bool = True,
    ) -> None:
        self.text = text
        self.rect = rect
        self.font = get_font(font_size)
        self.normal_color = normal_color
        self.active_color = active_color
        self.disabled_color = disabled_color
        self.text_color = text_color
        self.enabled = enabled

    def draw(self, screen: pygame.Surface, *, selected: bool = False) -> None:
        if not self.enabled:
            color = self.disabled_color
        else:
            color = self.active_color if selected else self.normal_color

        pygame.draw.rect(screen, color, self.rect, border_radius=6)
        pygame.draw.rect(screen, BACKGROUND_COLOR, self.rect, width=2, border_radius=6)
        surface = self.font.render(self.text, True, self.text_color)
        text_rect = surface.get_rect(center=self.rect.center)
        screen.blit(surface, text_rect)

    def contains(self, position: tuple[int, int]) -> bool:
        return self.enabled and self.rect.collidepoint(position)
