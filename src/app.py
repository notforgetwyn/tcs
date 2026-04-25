from __future__ import annotations

from pathlib import Path

import pygame

from src.constants import FPS, WINDOW_HEIGHT, WINDOW_TITLE, WINDOW_WIDTH
from src.core.input_debug import InputDebug
from src.core.input_service import InputService
from src.core.file_manager import FileManager
from src.core.save_service import SaveService
from src.core.settings_service import SettingsService
from src.models.game_state import GameState
from src.scenes.continue_scene import ContinueScene
from src.scenes.gameplay_scene import GameplayScene
from src.scenes.menu_scene import MenuScene
from src.scenes.settings_scene import SettingsScene


class App:
    """Owns the pygame lifecycle and the active scene."""

    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.is_running = True
        self.file_manager = FileManager(Path(__file__).resolve().parents[1])
        self.settings_service = SettingsService(self.file_manager)
        self.save_service = SaveService(self.file_manager)
        self.input_debug = InputDebug()
        self.input_service = InputService(self.file_manager)
        self.scenes = {
            "menu": MenuScene(self),
            "settings": SettingsScene(self),
            "continue": ContinueScene(self),
        }
        self.scene = self.scenes["menu"]
        self.scene.on_enter()
        self._update_window_title("menu")

    def run(self) -> None:
        while self.is_running:
            delta_ms = self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop()
                    break

                self.input_debug.record(event)

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
            self.scenes["continue"] = ContinueScene(self)
            scene_name = "continue"
        elif scene_name == "settings":
            self.scenes["settings"] = SettingsScene(self)
        target_scene = self.scenes.get(scene_name)
        if target_scene is not None:
            self.scene = target_scene
            self.scene.on_enter()
            self._update_window_title(scene_name)

    def stop(self) -> None:
        self.is_running = False

    def start_new_game(self) -> None:
        self.scenes["gameplay"] = GameplayScene(self)
        self.scene = self.scenes["gameplay"]
        self.scene.on_enter()
        self._update_window_title("gameplay")

    def load_gameplay_from_state(self, game_state: GameState, save_id: str | None = None) -> None:
        self.scenes["gameplay"] = GameplayScene(self, game_state=game_state, save_id=save_id)
        self.scene = self.scenes["gameplay"]
        self.scene.on_enter()
        self._update_window_title("gameplay")

    def _update_window_title(self, scene_name: str) -> None:
        pygame.display.set_caption(f"{WINDOW_TITLE} - {scene_name}")
