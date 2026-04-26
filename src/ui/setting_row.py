from __future__ import annotations

import pygame

from src.constants import BUTTON_ACTIVE_COLOR, TEXT_COLOR
from src.ui.text import TextBlock


class SettingRow:
    """Selectable text row used by settings screens."""

    def __init__(
        self,
        label: str,
        value: str,
        center: tuple[int, int],
        *,
        selected: bool = False,
        font_size: int = 24,
    ) -> None:
        self.label = label
        self.value = value
        self.center = center
        self.selected = selected
        self.font_size = font_size

    def draw(self, screen: pygame.Surface) -> None:
        marker = "> " if self.selected else "  "
        tail = " <" if self.selected else "  "
        color = BUTTON_ACTIVE_COLOR if self.selected else TEXT_COLOR
        TextBlock(f"{marker}{self.label}: {self.value}{tail}", self.font_size, color).draw_center(
            screen,
            self.center,
        )

    def hit_rect(self, width: int = 600, height: int = 32) -> pygame.Rect:
        return pygame.Rect(self.center[0] - width // 2, self.center[1] - height // 2, width, height)

    def contains(self, position: tuple[int, int]) -> bool:
        return self.hit_rect().collidepoint(position)
