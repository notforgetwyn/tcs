from __future__ import annotations

from copy import deepcopy

from src.constants import DOWN, LEFT, RIGHT, UP
from src.core import system_keys
from src.core.file_manager import FileManager


DEFAULT_KEY_BINDINGS: dict[str, list[str]] = {
    "debug_toggle": ["F3"],
    "confirm": ["RETURN", "SPACE"],
    "back": ["ESCAPE"],
    "menu_up": ["UP", "W"],
    "menu_down": ["DOWN", "S"],
    "settings_left": ["LEFT", "A"],
    "settings_right": ["RIGHT", "D"],
    "move_up": ["UP", "W"],
    "move_down": ["DOWN", "S"],
    "move_left": ["LEFT", "A"],
    "move_right": ["RIGHT", "D"],
    "save_game": ["E"],
    "pause_game": ["P"],
    "restart_game": ["R"],
}


SPECIAL_KEY_NAME_TO_VK: dict[str, int] = {
    "DOWN": system_keys.VK_DOWN,
    "ESCAPE": system_keys.VK_ESCAPE,
    "F3": system_keys.VK_F3,
    "LEFT": system_keys.VK_LEFT,
    "RETURN": system_keys.VK_RETURN,
    "RIGHT": system_keys.VK_RIGHT,
    "SPACE": system_keys.VK_SPACE,
    "UP": system_keys.VK_UP,
}

KEY_NAME_TO_VK: dict[str, int] = {
    **SPECIAL_KEY_NAME_TO_VK,
    **{chr(code): code for code in range(ord("A"), ord("Z") + 1)},
}

CAPTURE_KEY_NAMES = [
    "UP",
    "DOWN",
    "LEFT",
    "RIGHT",
    *[chr(code) for code in range(ord("A"), ord("Z") + 1)],
    "RETURN",
    "SPACE",
    "ESCAPE",
    "F3",
]


class InputService:
    """Centralizes key binding lookup and Windows key state reads."""

    def __init__(self, file_manager: FileManager) -> None:
        self.file_manager = file_manager
        self.key_edges = system_keys.KeyEdges()
        self.bindings = self._load_bindings()

    def just_pressed(self, action: str) -> bool:
        return self.key_edges.just_pressed(action, *self._virtual_keys(action))

    def pressed(self, action: str) -> bool:
        return system_keys.any_pressed(*self._virtual_keys(action))

    def sync(self, action: str) -> None:
        self.key_edges.sync(action, *self._virtual_keys(action))

    def sync_many(self, actions: list[str]) -> None:
        for action in actions:
            self.sync(action)

    def direction(self) -> tuple[int, int] | None:
        if self.pressed("move_up"):
            return UP
        if self.pressed("move_down"):
            return DOWN
        if self.pressed("move_left"):
            return LEFT
        if self.pressed("move_right"):
            return RIGHT
        return None

    def binding_text(self, action: str) -> str:
        return " / ".join(self.bindings.get(action, []))

    def capture_key_press(self) -> str | None:
        for key_name in CAPTURE_KEY_NAMES:
            virtual_key = KEY_NAME_TO_VK[key_name]
            if self.key_edges.just_pressed(f"capture:{key_name}", virtual_key):
                return key_name
        return None

    def sync_capture_keys(self) -> None:
        for key_name in CAPTURE_KEY_NAMES:
            self.key_edges.sync(f"capture:{key_name}", KEY_NAME_TO_VK[key_name])

    def set_single_binding(self, action: str, key_name: str) -> None:
        if action not in DEFAULT_KEY_BINDINGS or key_name not in KEY_NAME_TO_VK:
            return
        self.bindings[action] = [key_name]
        self.file_manager.save_json("config/key_bindings.json", self.bindings)
        self.sync(action)

    def action_using_key(self, key_name: str, *, exclude: str | None = None) -> str | None:
        for action, key_names in self.bindings.items():
            if action != exclude and key_name in key_names:
                return action
        return None

    def _load_bindings(self) -> dict[str, list[str]]:
        raw_data = self.file_manager.load_json("config/key_bindings.json", deepcopy(DEFAULT_KEY_BINDINGS))
        normalized: dict[str, list[str]] = {}

        for action, default_keys in DEFAULT_KEY_BINDINGS.items():
            keys = raw_data.get(action)
            if not isinstance(keys, list):
                normalized[action] = list(default_keys)
                continue

            valid_keys = [key for key in keys if isinstance(key, str) and key in KEY_NAME_TO_VK]
            normalized[action] = valid_keys or list(default_keys)

        if normalized != raw_data:
            self.file_manager.save_json("config/key_bindings.json", normalized)
        return normalized

    def _virtual_keys(self, action: str) -> list[int]:
        key_names = self.bindings.get(action, [])
        return [KEY_NAME_TO_VK[key_name] for key_name in key_names if key_name in KEY_NAME_TO_VK]
