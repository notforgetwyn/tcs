from __future__ import annotations

import pygame

from src.constants import BACKGROUND_COLOR, WINDOW_HEIGHT, WINDOW_WIDTH
from src.core.input_keys import is_down, is_up
from src.scenes.base_scene import BaseScene
from src.ui.menu_list import MenuList
from src.ui.text import TextBlock


class MenuScene(BaseScene):
    """Main menu scene used as the application's entry point."""

    def __init__(self, app) -> None:
        super().__init__(app)
        self.options = [
            ("\u5f00\u59cb\u6e38\u620f", "gameplay"),
            ("\u7ee7\u7eed\u6e38\u620f", "continue_game"),
            ("\u8bbe\u7f6e", "settings"),
            ("\u9000\u51fa\u6e38\u620f", "exit"),
        ]
        self.menu_list = MenuList([label for label, _ in self.options])

    def handle_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._handle_mouse_click(event.pos)
            return True

        if event.type != pygame.KEYDOWN:
            return True

        if is_up(event):
            self.menu_list.move_up()
        elif is_down(event):
            self.menu_list.move_down()
        elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
            self._activate_selected()
        elif event.key == pygame.K_ESCAPE:
            return False

        return True

    def render(self, screen: pygame.Surface) -> None:
        screen.fill(BACKGROUND_COLOR)
        TextBlock("\u8d2a\u5403\u86c7", 72).draw_center(screen, (WINDOW_WIDTH // 2, 120))
        self.menu_list.draw_centered(screen, WINDOW_WIDTH // 2, 240)
        TextBlock(
            "\u4f7f\u7528 W/S \u6216\u65b9\u5411\u952e\u9009\u62e9\uff0c\u6309 Enter \u786e\u8ba4",
            28,
        ).draw_center(screen, (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 70))

    def _activate_selected(self) -> None:
        _, action = self.options[self.menu_list.selected_index]
        if action == "gameplay":
            self.app.start_new_game()
            return
        if action == "exit":
            self.app.stop()
            return
        self.app.change_scene(action)

    def _handle_mouse_click(self, position: tuple[int, int]) -> None:
        selected = self.menu_list.hit_test(position, WINDOW_WIDTH // 2, 240)
        if selected is None:
            return
        self.menu_list.selected_index = selected
        self._activate_selected()
