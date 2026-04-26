from __future__ import annotations

import pygame

from src.constants import BUTTON_ACTIVE_COLOR, BUTTON_HOVER_COLOR, BUTTON_NORMAL_COLOR, TEXT_COLOR
from src.core.save_service import SaveSlot
from src.ui.button import Button
from src.ui.text import TextBlock


class SaveCard:
    """Visual card for one save slot, including action buttons."""

    def __init__(
        self,
        slot: SaveSlot,
        rect: pygame.Rect,
        *,
        display_index: int,
        selected: bool = False,
        hovered: bool = False,
    ) -> None:
        self.slot = slot
        self.rect = rect
        self.display_index = display_index
        self.selected = selected
        self.hovered = hovered

    def draw(self, screen: pygame.Surface) -> None:
        color = self._background_color()
        border_width = 3 if self.selected else 2 if self.hovered else 1
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, TEXT_COLOR, self.rect, width=border_width, border_radius=10)

        title = f"{self.display_index}. {self._short_text(self.slot.name, 18)}"
        summary = (
            f"\u5206\u6570:{self.slot.game_state.score}  "
            f"\u957f\u5ea6:{len(self.slot.game_state.snake_body)}  "
            f"\u66f4\u65b0:{self.slot.updated_at}"
        )
        TextBlock(title, 22, TEXT_COLOR).draw_topleft(screen, (self.rect.x + 16, self.rect.y + 7))
        TextBlock(summary, 18, TEXT_COLOR).draw_topleft(screen, (self.rect.x + 16, self.rect.y + 31))

        for action, button in self.action_buttons().items():
            button.draw(screen)

    def contains(self, position: tuple[int, int]) -> bool:
        return self.rect.collidepoint(position)

    def action_at(self, position: tuple[int, int]) -> str | None:
        for action, button in self.action_buttons().items():
            if button.contains(position):
                return action
        return None

    def action_buttons(self) -> dict[str, Button]:
        button_width = 72
        button_height = 24
        button_y = self.rect.y + 15
        delete_rect = pygame.Rect(self.rect.right - button_width - 12, button_y, button_width, button_height)
        rename_rect = pygame.Rect(delete_rect.x - button_width - 8, button_y, button_width, button_height)
        return {
            "rename": Button(
                "\u91cd\u547d\u540d",
                rename_rect,
                font_size=16,
                normal_color=(39, 174, 96),
                active_color=(39, 174, 96),
                hover_color=(39, 174, 96),
            ),
            "delete": Button(
                "\u5220\u9664",
                delete_rect,
                font_size=16,
                normal_color=(192, 57, 43),
                active_color=(192, 57, 43),
                hover_color=(192, 57, 43),
            ),
        }

    def _background_color(self) -> tuple[int, int, int]:
        if self.selected:
            return BUTTON_ACTIVE_COLOR
        if self.hovered:
            return BUTTON_HOVER_COLOR
        return BUTTON_NORMAL_COLOR

    def _short_text(self, text: str, limit: int) -> str:
        if len(text) <= limit:
            return text
        return text[: limit - 1] + "..."
