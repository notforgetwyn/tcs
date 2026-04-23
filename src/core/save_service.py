from __future__ import annotations

from src.core.file_manager import FileManager
from src.models.game_state import GameState


class SaveService:
    """Persists and restores resumable game state."""

    def __init__(self, file_manager: FileManager) -> None:
        self.file_manager = file_manager
        self._defaults = {"has_save": False, "game_state": None}

    def has_save(self) -> bool:
        raw_data = self.file_manager.load_json("data/save.json", self._defaults)
        return bool(raw_data.get("has_save"))

    def load(self) -> GameState | None:
        raw_data = self.file_manager.load_json("data/save.json", self._defaults)
        if not raw_data.get("has_save"):
            return None

        game_state = raw_data.get("game_state")
        if not isinstance(game_state, dict):
            self.clear()
            return None

        loaded = GameState.from_dict(game_state)
        if loaded is None:
            self.clear()
        return loaded

    def save(self, game_state: GameState) -> None:
        self.file_manager.save_json(
            "data/save.json",
            {
                "has_save": True,
                "game_state": game_state.to_dict(),
            },
        )

    def clear(self) -> None:
        self.file_manager.save_json("data/save.json", self._defaults)
