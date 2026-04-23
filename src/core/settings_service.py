from __future__ import annotations

from dataclasses import dataclass

from src.core.file_manager import FileManager


DEFAULT_MOVE_INTERVAL_MS = 140
MIN_MOVE_INTERVAL_MS = 60
MAX_MOVE_INTERVAL_MS = 260
MOVE_INTERVAL_STEP_MS = 20


@dataclass
class Settings:
    move_interval_ms: int = DEFAULT_MOVE_INTERVAL_MS


class SettingsService:
    """Loads and saves user settings from JSON."""

    def __init__(self, file_manager: FileManager) -> None:
        self.file_manager = file_manager
        self._defaults = {"move_interval_ms": DEFAULT_MOVE_INTERVAL_MS}

    def load(self) -> Settings:
        raw_data = self.file_manager.load_json("config/settings.json", self._defaults)
        move_interval_ms = self._sanitize_interval(raw_data.get("move_interval_ms"))
        settings = Settings(move_interval_ms=move_interval_ms)
        if raw_data.get("move_interval_ms") != move_interval_ms:
            self.save(settings)
        return settings

    def save(self, settings: Settings) -> None:
        payload = {
            "move_interval_ms": self._sanitize_interval(settings.move_interval_ms),
        }
        self.file_manager.save_json("config/settings.json", payload)

    def _sanitize_interval(self, value: object) -> int:
        if not isinstance(value, int):
            return DEFAULT_MOVE_INTERVAL_MS
        return max(MIN_MOVE_INTERVAL_MS, min(MAX_MOVE_INTERVAL_MS, value))
