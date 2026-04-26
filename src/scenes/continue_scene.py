from __future__ import annotations

import pygame

from src.constants import BACKGROUND_COLOR, BUTTON_NORMAL_COLOR, TEXT_COLOR, WINDOW_HEIGHT, WINDOW_WIDTH
from src.core.save_service import SaveSlot
from src.scenes.base_scene import BaseScene
from src.ui.button import Button
from src.ui.panel import Panel
from src.ui.save_card import SaveCard
from src.ui.scroll_list import ScrollList
from src.ui.text import TextBlock


class ContinueScene(BaseScene):
    """Shows multiple save slots and lets the player choose one to continue."""

    MAX_VISIBLE_SAVES = 5

    def __init__(self, app) -> None:
        super().__init__(app)
        self.save_slots = self.app.save_service.list_saves()
        self.save_list = ScrollList(self.MAX_VISIBLE_SAVES)
        self.save_list.configure(len(self.save_slots), extra_selectable_count=1)
        self.hovered_index: int | None = None
        self.pending_delete_id: str | None = None
        self.rename_save_id: str | None = None
        self.rename_buffer = ""
        self.status_message = "\u9009\u62e9\u5b58\u6863\u540e Enter \u8bfb\u53d6\uff0cN \u91cd\u547d\u540d\uff0cDelete \u5220\u9664\u3002"

    def handle_event(self, event: pygame.event.Event) -> bool:
        if self.rename_save_id is not None:
            if event.type == pygame.TEXTINPUT:
                self._append_rename_text(event.text)
            return True
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._handle_mouse_click(event.pos)
        elif event.type == pygame.MOUSEWHEEL:
            self._scroll(-event.y)
        elif event.type == pygame.MOUSEMOTION:
            self._handle_mouse_motion(event.pos)
        return True

    def on_enter(self) -> None:
        self.save_slots = self.app.save_service.list_saves()
        self.save_list.configure(len(self.save_slots), extra_selectable_count=1)
        self.pending_delete_id = None
        self.rename_save_id = None
        self.rename_buffer = ""
        self.app.input_service.sync_many(
            ["debug_toggle", "menu_up", "menu_down", "confirm", "back", "delete_save", "rename_save"]
        )

    def update(self, delta_ms: int) -> None:
        _ = delta_ms
        if self.rename_save_id is not None:
            self._update_rename_mode()
            return

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
        elif self.app.input_service.just_pressed("rename_save"):
            self.app.input_debug.record_system_key("rename")
            self._start_rename()
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
            for visible_index, (actual_index, slot) in enumerate(self.save_list.visible_items(self.save_slots)):
                self._save_card(slot, actual_index, visible_index).draw(screen)

        self._draw_back_button(screen)
        if self.rename_save_id is not None:
            self._draw_rename_panel(screen)
        TextBlock(self.status_message, 24).draw_center(screen, (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 34))

        if self.app.input_debug.enabled:
            TextBlock(self.app.input_debug.last_key_text, 20).draw_topleft(screen, (16, WINDOW_HEIGHT - 32))

    def _draw_scroll_status(self, screen: pygame.Surface) -> None:
        total = len(self.save_slots)
        start, end, total = self.save_list.scroll_status()
        text = f"\u663e\u793a {start}-{end} / {total}  \u6eda\u8f6e/W/S \u6d4f\u89c8\uff0cN \u91cd\u547d\u540d\uff0cDelete \u5220\u9664"
        TextBlock(text, 22, TEXT_COLOR).draw_center(screen, (WINDOW_WIDTH // 2, 170))

    def _save_card_rect(self, visible_index: int) -> pygame.Rect:
        button_width = 600
        button_height = 54
        center_x = WINDOW_WIDTH // 2
        y = 185 + visible_index * 60
        return pygame.Rect(center_x - button_width // 2, y, button_width, button_height)

    def _save_card(self, slot: SaveSlot, actual_index: int, visible_index: int) -> SaveCard:
        return SaveCard(
            slot,
            self._save_card_rect(visible_index),
            display_index=actual_index + 1,
            selected=actual_index == self.save_list.selected_index,
            hovered=actual_index == self.hovered_index,
        )

    def _back_button_rect(self) -> pygame.Rect:
        button_width = 260
        button_height = 52
        center_x = WINDOW_WIDTH // 2
        return pygame.Rect(center_x - button_width // 2, 520, button_width, button_height)

    def _draw_back_button(self, screen: pygame.Surface) -> None:
        rect = self._back_button_rect()
        selected = self.save_list.selected_index == len(self.save_slots)
        hovered = self.hovered_index == len(self.save_slots)
        Button("\u8fd4\u56de\u4e3b\u83dc\u5355", rect, font_size=30, normal_color=BUTTON_NORMAL_COLOR).draw(
            screen,
            selected=selected,
            hovered=hovered,
        )

    def _draw_rename_panel(self, screen: pygame.Surface) -> None:
        panel_rect = pygame.Rect(120, 408, 560, 82)
        Panel(panel_rect).draw(screen)
        TextBlock("\u8f93\u5165\u65b0\u5b58\u6863\u540d\uff1a", 22, TEXT_COLOR).draw_topleft(screen, (panel_rect.x + 16, panel_rect.y + 12))
        display_name = self.rename_buffer or "\u672a\u547d\u540d"
        TextBlock(display_name, 26, TEXT_COLOR).draw_topleft(screen, (panel_rect.x + 16, panel_rect.y + 42))

    def _move_selection(self, step: int) -> None:
        self.save_list.move_selection(step)
        self.hovered_index = None
        self.pending_delete_id = None

    def _activate_selected(self) -> None:
        if self.save_list.selected_index < len(self.save_slots):
            slot = self.save_slots[self.save_list.selected_index]
            self.app.load_gameplay_from_state(slot.game_state, save_id=slot.save_id)
            return
        self.app.change_scene("menu")

    def _start_rename(self) -> None:
        if self.save_list.selected_index >= len(self.save_slots):
            self.status_message = "\u8bf7\u5148\u9009\u62e9\u8981\u91cd\u547d\u540d\u7684\u5b58\u6863\u3002"
            return
        slot = self.save_slots[self.save_list.selected_index]
        self.rename_save_id = slot.save_id
        self.rename_buffer = slot.name
        self.pending_delete_id = None
        self.status_message = "\u8f93\u5165\u65b0\u540d\u79f0\uff0cEnter \u4fdd\u5b58\uff0cEsc \u53d6\u6d88\uff0cBackspace \u5220\u9664\u3002"
        self.app.input_service.sync_key("RETURN")
        self.app.input_service.sync_key("ESCAPE")
        self.app.input_service.sync_key("BACKSPACE")
        pygame.key.start_text_input()

    def _update_rename_mode(self) -> None:
        if self.app.input_service.just_pressed_key("RETURN"):
            self._confirm_rename()
        elif self.app.input_service.just_pressed_key("ESCAPE"):
            self._cancel_rename()
        elif self.app.input_service.just_pressed_key("BACKSPACE"):
            self.rename_buffer = self.rename_buffer[:-1]

    def _append_rename_text(self, text: str) -> None:
        if not isinstance(text, str) or not text:
            return
        cleaned = "".join(ch for ch in text if ch.isprintable())
        if not cleaned:
            return
        self.rename_buffer = (self.rename_buffer + cleaned)[:24]

    def _confirm_rename(self) -> None:
        if self.rename_save_id is None:
            return
        next_name = self.rename_buffer.strip()
        if not next_name:
            self.status_message = "\u5b58\u6863\u540d\u4e0d\u80fd\u4e3a\u7a7a\u3002"
            return
        self.app.save_service.rename(self.rename_save_id, next_name)
        self.save_slots = self.app.save_service.list_saves()
        self.rename_save_id = None
        self.rename_buffer = ""
        pygame.key.stop_text_input()
        self.status_message = f"\u5df2\u91cd\u547d\u540d\u4e3a\u3010{next_name}\u3011\u3002"

    def _cancel_rename(self) -> None:
        self.rename_save_id = None
        self.rename_buffer = ""
        pygame.key.stop_text_input()
        self.status_message = "\u5df2\u53d6\u6d88\u91cd\u547d\u540d\u3002"

    def _request_or_confirm_delete(self) -> None:
        if self.save_list.selected_index >= len(self.save_slots):
            self.status_message = "\u8bf7\u5148\u9009\u62e9\u8981\u5220\u9664\u7684\u5b58\u6863\u3002"
            return

        slot = self.save_slots[self.save_list.selected_index]
        if self.pending_delete_id != slot.save_id:
            self.pending_delete_id = slot.save_id
            self.status_message = f"\u518d\u6309\u4e00\u6b21 Delete \u786e\u8ba4\u5220\u9664\u3010{slot.name}\u3011\uff1bEsc \u53d6\u6d88\u3002"
            return

        self.app.save_service.delete(slot.save_id)
        deleted_name = slot.name
        self.save_slots = self.app.save_service.list_saves()
        self.save_list.configure(len(self.save_slots), extra_selectable_count=1)
        self.pending_delete_id = None
        self.status_message = f"\u5df2\u5220\u9664\u5b58\u6863\u3010{deleted_name}\u3011\u3002"

    def _handle_mouse_click(self, position: tuple[int, int]) -> None:
        action_hit = self._hit_test_action(position)
        if action_hit is not None:
            action, actual_index = action_hit
            self.save_list.selected_index = actual_index
            self.hovered_index = actual_index
            if action == "rename":
                self._start_rename()
            else:
                self._request_or_confirm_delete()
            return

        hit_index = self._hit_test(position)
        if hit_index is None:
            return
        self.save_list.selected_index = hit_index
        self.pending_delete_id = None
        self.rename_save_id = None
        self._activate_selected()

    def _handle_mouse_motion(self, position: tuple[int, int]) -> None:
        self.hovered_index = self._hit_test(position)
        if self.hovered_index is not None:
            self.save_list.selected_index = self.hovered_index
            self.save_list.sync_to_selection()

    def _scroll(self, step: int) -> None:
        self.save_list.scroll(step)
        self.hovered_index = None
        self.pending_delete_id = None
        self.rename_save_id = None

    def _hit_test(self, position: tuple[int, int]) -> int | None:
        for visible_index, (actual_index, _slot) in enumerate(self.save_list.visible_items(self.save_slots)):
            if self._save_card_rect(visible_index).collidepoint(position):
                return actual_index
        if self._back_button_rect().collidepoint(position):
            return len(self.save_slots)
        return None

    def _hit_test_action(self, position: tuple[int, int]) -> tuple[str, int] | None:
        for visible_index, (actual_index, slot) in enumerate(self.save_list.visible_items(self.save_slots)):
            action = self._save_card(slot, actual_index, visible_index).action_at(position)
            if action is not None:
                return action, actual_index
        return None
