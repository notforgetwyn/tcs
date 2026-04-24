from __future__ import annotations

from pathlib import Path

import pygame

from src.constants import FPS, WINDOW_HEIGHT, WINDOW_TITLE, WINDOW_WIDTH
from src.core.file_manager import FileManager
from src.core.save_service import SaveService
from src.core.settings_service import SettingsService
from src.models.game_state import GameState
from src.scenes.gameplay_scene import GameplayScene
from src.scenes.menu_scene import MenuScene
from src.scenes.placeholder_scene import PlaceholderScene
from src.scenes.settings_scene import SettingsScene


class App:
    """Owns the pygame lifecycle and the active scene."""

    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption(WINDOW_TITLE)
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.is_running = True
        self.file_manager = FileManager(Path(__file__).resolve().parents[1])
        self.settings_service = SettingsService(self.file_manager)
        self.save_service = SaveService(self.file_manager)
        self.scenes = {
            "menu": MenuScene(self),
            "gameplay": GameplayScene(self),
            "settings": SettingsScene(self),
            "continue_unavailable": PlaceholderScene(
                self,
                title="\u7ee7\u7eed\u6e38\u620f",
                message="\u5f53\u524d\u6ca1\u6709\u53ef\u7ee7\u7eed\u7684\u5b58\u6863\u3002",
            ),
        }
        self.scene = self.scenes["menu"]

    def run(self) -> None:
        while self.is_running:
            delta_ms = self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop()
                    break

                if not self.scene.handle_event(event):
                    self.stop()
                    break

            if not self.is_running:
                continue

            self.scene.update(delta_ms)
            self.scene.render(self.screen)
            pygame.display.flip()

        pygame.quit()

    def change_scene(self, scene_name: str) -> None:
        if scene_name == "gameplay":
            self.scenes["gameplay"] = GameplayScene(self)
        elif scene_name == "continue_game":
            self._continue_game()
            return
        elif scene_name == "settings":
            self.scenes["settings"] = SettingsScene(self)
        target_scene = self.scenes.get(scene_name)
        if target_scene is not None:
            self.scene = target_scene

    def stop(self) -> None:
        self.is_running = False

    def start_new_game(self) -> None:
        self.save_service.clear()
        self.scenes["gameplay"] = GameplayScene(self)
        self.scene = self.scenes["gameplay"]

    def load_gameplay_from_state(self, game_state: GameState) -> None:
        self.scenes["gameplay"] = GameplayScene(self, game_state=game_state)
        self.scene = self.scenes["gameplay"]

    def show_continue_unavailable(
        self,
        message: str = "\u5f53\u524d\u6ca1\u6709\u53ef\u7ee7\u7eed\u7684\u5b58\u6863\u3002",
    ) -> None:
        self.scenes["continue_unavailable"] = PlaceholderScene(
            self,
            title="\u7ee7\u7eed\u6e38\u620f",
            message=message,
        )
        self.scene = self.scenes["continue_unavailable"]

    def _continue_game(self) -> None:
        loaded = self.save_service.load()
        if loaded is None:
            self.show_continue_unavailable()
            return
        self.load_gameplay_from_state(loaded)
