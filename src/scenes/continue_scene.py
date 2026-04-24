from __future__ import annotations

import pygame

from src.constants import BACKGROUND_COLOR, TEXT_COLOR, WINDOW_HEIGHT, WINDOW_WIDTH
from src.core import system_keys
from src.models.game_state import GameState
from src.scenes.base_scene import BaseScene
from src.ui.button import Button
from src.ui.text import TextBlock


class ContinueScene(BaseScene):
    """Shows save status and lets the player continue when a save exists."""

    def __init__(self, app) -> None:
        super().__init__(app)
        self.game_state = self.app.save_service.load()
        self.buttons = self._build_buttons()
        self.selected_index = 0
        self.hovered_index: int | None = None
        self.key_edges = system_keys.KeyEdges()

    def handle_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._handle_mouse_click(event.pos)
        elif event.type == pygame.MOUSEMOTION:
            self._handle_mouse_motion(event.pos)
        return True

    def update(self, delta_ms: int) -> None:
        _ = delta_ms
        if self.key_edges.just_pressed("f3", system_keys.VK_F3):
            self.app.input_debug.enabled = not self.app.input_debug.enabled
            self.app.input_debug.record_system_key("f3")
        elif self.key_edges.just_pressed("up", system_keys.VK_UP, system_keys.VK_W):
            self._move_selection(-1)
            self.app.input_debug.record_system_key("up")
        elif self.key_edges.just_pressed("down", system_keys.VK_DOWN, system_keys.VK_S):
            self._move_selection(1)
            self.app.input_debug.record_system_key("down")
        elif self.key_edges.just_pressed("confirm", system_keys.VK_RETURN, system_keys.VK_SPACE):
            self.app.input_debug.record_system_key("confirm")
            self._activate_selected()
        elif self.key_edges.just_pressed("escape", system_keys.VK_ESCAPE):
            self.app.input_debug.record_system_key("escape")
            self.app.change_scene("menu")

    def render(self, screen: pygame.Surface) -> None:
        screen.fill(BACKGROUND_COLOR)
        center_x = WINDOW_WIDTH // 2
        TextBlock("\u7ee7\u7eed\u6e38\u620f", 64).draw_center(screen, (center_x, 110))

        if self.game_state is None:
            TextBlock("\u5f53\u524d\u6ca1\u6709\u53ef\u7ee7\u7eed\u7684\u5b58\u6863\u3002", 34).draw_center(
                screen,
                (center_x, 220),
            )
            TextBlock("\u8bf7\u8fd4\u56de\u4e3b\u83dc\u5355\u5f00\u59cb\u65b0\u6e38\u620f\u3002", 28).draw_center(
                screen,
                (center_x, 265),
            )
        else:
            self._draw_save_summary(screen, self.game_state)

        for index, button in enumerate(self.buttons):
            button.draw(
                screen,
                selected=index == self.selected_index,
                hovered=index == self.hovered_index,
            )

        if self.app.input_debug.enabled:
            TextBlock(self.app.input_debug.last_key_text, 20).draw_topleft(screen, (16, WINDOW_HEIGHT - 32))

    def _build_buttons(self) -> list[Button]:
        button_width = 240
        button_height = 52
        center_x = WINDOW_WIDTH // 2
        start_y = 360

        buttons: list[Button] = []
        if self.game_state is not None:
            buttons.append(
                Button(
                    "\u7ee7\u7eed\u6e38\u620f",
                    pygame.Rect(center_x - button_width // 2, start_y, button_width, button_height),
                )
            )
            start_y += 70

        buttons.append(
            Button(
                "\u8fd4\u56de\u4e3b\u83dc\u5355",
                pygame.Rect(center_x - button_width // 2, start_y, button_width, button_height),
            )
        )
        return buttons

    def _draw_save_summary(self, screen: pygame.Surface, game_state: GameState) -> None:
        center_x = WINDOW_WIDTH // 2
        TextBlock("\u5df2\u627e\u5230\u53ef\u7ee7\u7eed\u7684\u5b58\u6863", 34).draw_center(screen, (center_x, 205))
        TextBlock(f"\u5f53\u524d\u5206\u6570: {game_state.score}", 30, TEXT_COLOR).draw_center(
            screen,
            (center_x, 255),
        )
        TextBlock(
            f"\u86c7\u8eab\u957f\u5ea6: {len(game_state.snake_body)}    \u901f\u5ea6: {game_state.move_interval_ms} ms",
            28,
        ).draw_center(screen, (center_x, 300))

    def _move_selection(self, step: int) -> None:
        self.selected_index = (self.selected_index + step) % len(self.buttons)

    def _activate_selected(self) -> None:
        label = self.buttons[self.selected_index].text
        if label == "\u7ee7\u7eed\u6e38\u620f" and self.game_state is not None:
            self.app.load_gameplay_from_state(self.game_state)
            return
        self.app.change_scene("menu")

    def _handle_mouse_click(self, position: tuple[int, int]) -> None:
        for index, button in enumerate(self.buttons):
            if button.contains(position):
                self.selected_index = index
                self._activate_selected()
                return

    def _handle_mouse_motion(self, position: tuple[int, int]) -> None:
        self.hovered_index = None
        for index, button in enumerate(self.buttons):
            if button.contains(position):
                self.hovered_index = index
                self.selected_index = index
                return
