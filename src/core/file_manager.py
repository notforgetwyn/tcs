from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class FileManager:
    """Handles safe JSON file access with default fallbacks."""

    def __init__(self, base_dir: Path) -> None:
        self.base_dir = base_dir

    def load_json(self, relative_path: str, default_data: dict[str, Any]) -> dict[str, Any]:
        file_path = self.base_dir / relative_path
        try:
            if not file_path.exists():
                self.save_json(relative_path, default_data)
                return dict(default_data)

            with file_path.open("r", encoding="utf-8") as file:
                data = json.load(file)

            if not isinstance(data, dict):
                raise ValueError("JSON root must be an object.")

            return data
        except (OSError, json.JSONDecodeError, ValueError):
            self.save_json(relative_path, default_data)
            return dict(default_data)

    def save_json(self, relative_path: str, data: dict[str, Any]) -> None:
        file_path = self.base_dir / relative_path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with file_path.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
