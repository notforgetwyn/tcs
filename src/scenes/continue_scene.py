from __future__ import annotations

import pygame

from src.constants import BACKGROUND_COLOR, TEXT_COLOR, WINDOW_HEIGHT, WINDOW_WIDTH
from src.core.save_service import SaveSlot
from src.scenes.base_scene import BaseScene
from src.ui.text import TextBlock


class ContinueScene(BaseScene):
    """Shows multiple save slots and lets the player choose one to continue."""

    MAX_VISIBLE_SAVES = 5

    def __init__(self, app) -> None:
        super().__init__(app)
        self.save_slots = self.app.save_service.list_saves()
        self.selected_index = 0
        self.hovered_index: int | None = None
        self.scroll_offset = 0
        self.pending_delete_id: str | None = None
        self.status_message = "\u9009\u62e9\u5b58\u6863\u540e Enter \u8bfb\u53d6\uff0cDelete \u5220\u9664\u3002"

    def handle_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._handle_mouse_click(event.pos)
        elif event.type == pygame.MOUSEWHEEL:
            self._scroll(-event.y)
        elif event.type == pygame.MOUSEMOTION:
            self._handle_mouse_motion(event.pos)
        return True

    def on_enter(self) -> None:
        self.save_slots = self.app.save_service.list_saves()
        self.selected_index = min(self.selected_index, self._last_index())
        self._sync_scroll_to_selection()
        self.pending_delete_id = None
        self.app.input_service.sync_many(["debug_toggle", "menu_up", "menu_down", "confirm", "back", "delete_save"])

    def update(self, delta_ms: int) -> None:
        _ = delta_ms
        if self.app.input_service.just_pressed("debug_toggle"):
            self.app.input_debug.enabled = not self.app.input_debug.enabled
            self.app.input_debug.record_system_key("f3")
        elif self.app.input_service.just_pressed("menu_up"):
            self._move_selection(-1)
            self.app.input_debug.record_system_key("up")
        elif self.app.input_service.just_pressed("menu_down"):
            self._move_selection(1)
            self.app.input_debug.record_system_key("down")
        elif self.app.input_service.just_pressed("confirm"):
            self.app.input_debug.record_system_key("confirm")
            self._activate_selected()
        elif self.app.input_service.just_pressed("delete_save"):
            self.app.input_debug.record_system_key("delete")
            self._request_or_confirm_delete()
        elif self.app.input_service.just_pressed("back"):
            self.app.input_debug.record_system_key("escape")
            if self.pending_delete_id is not None:
                self.pending_delete_id = None
                self.status_message = "\u5df2\u53d6\u6d88\u5220\u9664\u3002"
            else:
                self.app.change_scene("menu")

    def render(self, screen: pygame.Surface) -> None:
        screen.fill(BACKGROUND_COLOR)
        center_x = WINDOW_WIDTH // 2
        TextBlock("\u7ee7\u7eed\u6e38\u620f", 64).draw_center(screen, (center_x, 90))

        if not self.save_slots:
            TextBlock("\u5f53\u524d\u6ca1\u6709\u53ef\u7ee7\u7eed\u7684\u5b58\u6863\u3002", 34).draw_center(
                screen,
                (center_x, 220),
            )
            TextBlock("\u8bf7\u8fd4\u56de\u4e3b\u83dc\u5355\u5f00\u59cb\u65b0\u6e38\u620f\u3002", 28).draw_center(
                screen,
                (center_x, 265),
            )
        else:
            TextBlock("\u9009\u62e9\u8981\u8bfb\u53d6\u7684\u5b58\u6863", 28, TEXT_COLOR).draw_center(
                screen,
                (center_x, 145),
            )
            self._draw_scroll_status(screen)
            for visible_index, slot in enumerate(self._visible_slots()):
                actual_index = self.scroll_offset + visible_index
                self._draw_save_card(screen, slot, actual_index, visible_index)

        self._draw_back_button(screen)
        TextBlock(self.status_message, 24).draw_center(screen, (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 34))

        if self.app.input_debug.enabled:
            TextBlock(self.app.input_debug.last_key_text, 20).draw_topleft(screen, (16, WINDOW_HEIGHT - 32))

    def _draw_scroll_status(self, screen: pygame.Surface) -> None:
        total = len(self.save_slots)
        start = self.scroll_offset + 1
        end = min(self.scroll_offset + self.MAX_VISIBLE_SAVES, total)
        text = f"\u663e\u793a {start}-{end} / {total}  \u6eda\u8f6e\u6216 W/S \u6d4f\u89c8\uff0cDelete \u5220\u9664\u5b58\u6863"
        TextBlock(text, 22, TEXT_COLOR).draw_center(screen, (WINDOW_WIDTH // 2, 170))

    def _visible_slots(self) -> list[SaveSlot]:
        return self.save_slots[self.scroll_offset : self.scroll_offset + self.MAX_VISIBLE_SAVES]

    def _save_card_rect(self, visible_index: int) -> pygame.Rect:
        button_width = 600
        button_height = 54
        center_x = WINDOW_WIDTH // 2
        y = 185 + visible_index * 60
        return pygame.Rect(center_x - button_width // 2, y, button_width, button_height)

    def _draw_save_card(self, screen: pygame.Surface, slot: SaveSlot, actual_index: int, visible_index: int) -> None:
        rect = self._save_card_rect(visible_index)
        selected = actual_index == self.selected_index
        hovered = actual_index == self.hovered_index
        if selected:
            color = (52, 152, 219)
            border_width = 3
        elif hovered:
            color = (41, 128, 185)
            border_width = 2
        else:
            color = (44, 62, 80)
            border_width = 1

        pygame.draw.rect(screen, color, rect, border_radius=10)
        pygame.draw.rect(screen, TEXT_COLOR, rect, width=border_width, border_radius=10)

        title = f"{actual_index + 1}. {self._short_text(slot.name, 24)}"
        summary = f"\u5206\u6570:{slot.game_state.score}  \u957f\u5ea6:{len(slot.game_state.snake_body)}  \u66f4\u65b0:{slot.updated_at}"
        TextBlock(title, 22, TEXT_COLOR).draw_topleft(screen, (rect.x + 16, rect.y + 7))
        TextBlock(summary, 18, TEXT_COLOR).draw_topleft(screen, (rect.x + 16, rect.y + 31))

    def _back_button_rect(self) -> pygame.Rect:
        button_width = 260
        button_height = 52
        center_x = WINDOW_WIDTH // 2
        return pygame.Rect(center_x - button_width // 2, 520, button_width, button_height)

    def _draw_back_button(self, screen: pygame.Surface) -> None:
        rect = self._back_button_rect()
        selected = self.selected_index == len(self.save_slots)
        hovered = self.hovered_index == len(self.save_slots)
        color = (52, 152, 219) if selected else (41, 128, 185) if hovered else (44, 62, 80)
        border_width = 3 if selected else 2 if hovered else 1
        pygame.draw.rect(screen, color, rect, border_radius=10)
        pygame.draw.rect(screen, TEXT_COLOR, rect, width=border_width, border_radius=10)
        TextBlock("\u8fd4\u56de\u4e3b\u83dc\u5355", 30, TEXT_COLOR).draw_center(screen, rect.center)

    def _move_selection(self, step: int) -> None:
        self.selected_index = (self.selected_index + step) % (len(self.save_slots) + 1)
        self._sync_scroll_to_selection()
        self.hovered_index = None
        self.pending_delete_id = None

    def _activate_selected(self) -> None:
        if self.selected_index < len(self.save_slots):
            slot = self.save_slots[self.selected_index]
            self.app.load_gameplay_from_state(slot.game_state, save_id=slot.save_id)
            return
        self.app.change_scene("menu")

    def _request_or_confirm_delete(self) -> None:
        if self.selected_index >= len(self.save_slots):
            self.status_message = "\u8bf7\u5148\u9009\u62e9\u8981\u5220\u9664\u7684\u5b58\u6863\u3002"
            return

        slot = self.save_slots[self.selected_index]
        if self.pending_delete_id != slot.save_id:
            self.pending_delete_id = slot.save_id
            self.status_message = f"\u518d\u6309\u4e00\u6b21 Delete \u786e\u8ba4\u5220\u9664\u3010{slot.name}\u3011\uff1bEsc \u53d6\u6d88\u3002"
            return

        self.app.save_service.delete(slot.save_id)
        deleted_name = slot.name
        self.save_slots = self.app.save_service.list_saves()
        self.selected_index = min(self.selected_index, self._last_index())
        self.scroll_offset = min(self.scroll_offset, max(0, len(self.save_slots) - self.MAX_VISIBLE_SAVES))
        self._sync_scroll_to_selection()
        self.pending_delete_id = None
        self.status_message = f"\u5df2\u5220\u9664\u5b58\u6863\u3010{deleted_name}\u3011\u3002"

    def _handle_mouse_click(self, position: tuple[int, int]) -> None:
        hit_index = self._hit_test(position)
        if hit_index is None:
            return
        self.selected_index = hit_index
        self.pending_delete_id = None
        self._activate_selected()

    def _handle_mouse_motion(self, position: tuple[int, int]) -> None:
        self.hovered_index = self._hit_test(position)
        if self.hovered_index is not None:
            self.selected_index = self.hovered_index
            self._sync_scroll_to_selection()

    def _scroll(self, step: int) -> None:
        if len(self.save_slots) <= self.MAX_VISIBLE_SAVES:
            return

        max_offset = len(self.save_slots) - self.MAX_VISIBLE_SAVES
        self.scroll_offset = max(0, min(max_offset, self.scroll_offset + step))

        if self.selected_index < self.scroll_offset:
            self.selected_index = self.scroll_offset
        elif self.selected_index >= self.scroll_offset + self.MAX_VISIBLE_SAVES:
            self.selected_index = self.scroll_offset + self.MAX_VISIBLE_SAVES - 1
        self.hovered_index = None
        self.pending_delete_id = None

    def _hit_test(self, position: tuple[int, int]) -> int | None:
        for visible_index, slot in enumerate(self._visible_slots()):
            actual_index = self.scroll_offset + visible_index
            if self._save_card_rect(visible_index).collidepoint(position):
                return actual_index
        if self._back_button_rect().collidepoint(position):
            return len(self.save_slots)
        return None

    def _sync_scroll_to_selection(self) -> None:
        if self.selected_index >= len(self.save_slots):
            return
        if self.selected_index < self.scroll_offset:
            self.scroll_offset = self.selected_index
        elif self.selected_index >= self.scroll_offset + self.MAX_VISIBLE_SAVES:
            self.scroll_offset = self.selected_index - self.MAX_VISIBLE_SAVES + 1

    def _last_index(self) -> int:
        return len(self.save_slots)

    def _short_text(self, text: str, limit: int) -> str:
        if len(text) <= limit:
            return text
        return text[: limit - 1] + "..."
