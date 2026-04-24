from __future__ import annotations

import pygame

from src.constants import BACKGROUND_COLOR, WINDOW_HEIGHT, WINDOW_WIDTH
from src.scenes.base_scene import BaseScene
from src.ui.menu_list import MenuList
from src.ui.text import TextBlock


class MenuScene(BaseScene):
    """Main menu scene used as the application's entry point."""

    def __init__(self, app) -> None:
        super().__init__(app)
        self.options = [
            ("开始游戏", "gameplay"),
            ("继续游戏", "continue_game"),
            ("设置", "settings"),
            ("退出游戏", "exit"),
        ]
        self.menu_list = MenuList([label for label, _ in self.options])

    def handle_event(self, event: pygame.event.Event) -> bool:
        if event.type != pygame.KEYDOWN:
            return True

        if event.key in (pygame.K_UP, pygame.K_w):
            self.menu_list.move_up()
        elif event.key in (pygame.K_DOWN, pygame.K_s):
            self.menu_list.move_down()
        elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
            self._activate_selected()
        elif event.key == pygame.K_ESCAPE:
            return False

        return True

    def render(self, screen: pygame.Surface) -> None:
        screen.fill(BACKGROUND_COLOR)
        TextBlock("贪吃蛇", 72).draw_center(screen, (WINDOW_WIDTH // 2, 120))
        self.menu_list.draw_centered(screen, WINDOW_WIDTH // 2, 240)
        TextBlock("使用 W/S 或方向键选择，按 Enter 确认", 28).draw_center(
            screen,
            (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 70),
        )

    def _activate_selected(self) -> None:
        _, action = self.options[self.menu_list.selected_index]
        if action == "gameplay":
            self.app.start_new_game()
            return
        if action == "exit":
            self.app.stop()
            return
        self.app.change_scene(action)
