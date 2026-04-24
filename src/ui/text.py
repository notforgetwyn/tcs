from __future__ import annotations

import pygame

from src.constants import TEXT_COLOR
from src.ui.font_manager import get_font


class TextBlock:
    """Small helper for centered text rendering."""

    def __init__(self, text: str, size: int, color: tuple[int, int, int] = TEXT_COLOR) -> None:
        self.text = text
        self.font = get_font(size)
        self.color = color

    def draw_center(self, screen: pygame.Surface, center: tuple[int, int]) -> None:
        surface = self.font.render(self.text, True, self.color)
        rect = surface.get_rect(center=center)
        screen.blit(surface, rect)

    def draw_topleft(self, screen: pygame.Surface, position: tuple[int, int]) -> None:
        surface = self.font.render(self.text, True, self.color)
        screen.blit(surface, position)
