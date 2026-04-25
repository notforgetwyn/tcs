from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4

from src.core.file_manager import FileManager
from src.models.game_state import GameState


@dataclass(frozen=True)
class SaveSlot:
    save_id: str
    name: str
    created_at: str
    updated_at: str
    game_state: GameState


class SaveService:
    """Persists and restores multiple resumable game states."""

    def __init__(self, file_manager: FileManager) -> None:
        self.file_manager = file_manager
        self._defaults = {"saves": []}

    def has_save(self) -> bool:
        return bool(self.list_saves())

    def list_saves(self) -> list[SaveSlot]:
        raw_data = self.file_manager.load_json("data/save.json", self._defaults)
        saves = raw_data.get("saves")

        if not isinstance(saves, list):
            migrated = self._migrate_legacy_save(raw_data)
            if migrated is None:
                self.clear()
                return []
            self._write_slots([migrated])
            return [migrated]

        slots: list[SaveSlot] = []
        for item in saves:
            slot = self._parse_slot(item)
            if slot is not None:
                slots.append(slot)
        slots.sort(key=lambda slot: slot.updated_at, reverse=True)
        return slots

    def load(self, save_id: str | None = None) -> GameState | None:
        slots = self.list_saves()
        if not slots:
            return None
        if save_id is None:
            return slots[0].game_state
        for slot in slots:
            if slot.save_id == save_id:
                return slot.game_state
        return None

    def save(self, game_state: GameState, save_id: str | None = None) -> str:
        slots = self.list_saves()
        now = self._now()
        next_save_id = save_id or uuid4().hex
        updated_slots: list[SaveSlot] = []
        matched = False

        for slot in slots:
            if slot.save_id == next_save_id:
                updated_slots.append(
                    SaveSlot(
                        save_id=slot.save_id,
                        name=slot.name,
                        created_at=slot.created_at,
                        updated_at=now,
                        game_state=game_state,
                    )
                )
                matched = True
            else:
                updated_slots.append(slot)

        if not matched:
            updated_slots.append(
                SaveSlot(
                    save_id=next_save_id,
                    name=self._default_name(now),
                    created_at=now,
                    updated_at=now,
                    game_state=game_state,
                )
            )

        updated_slots.sort(key=lambda slot: slot.updated_at, reverse=True)
        self._write_slots(updated_slots)
        return next_save_id

    def delete(self, save_id: str) -> None:
        self._write_slots([slot for slot in self.list_saves() if slot.save_id != save_id])

    def rename(self, save_id: str, name: str) -> None:
        cleaned_name = name.strip()[:24]
        if not cleaned_name:
            return
        slots: list[SaveSlot] = []
        for slot in self.list_saves():
            if slot.save_id == save_id:
                slots.append(
                    SaveSlot(
                        save_id=slot.save_id,
                        name=cleaned_name,
                        created_at=slot.created_at,
                        updated_at=slot.updated_at,
                        game_state=slot.game_state,
                    )
                )
            else:
                slots.append(slot)
        self._write_slots(slots)

    def clear(self) -> None:
        self.file_manager.save_json("data/save.json", self._defaults)

    def _write_slots(self, slots: list[SaveSlot]) -> None:
        self.file_manager.save_json(
            "data/save.json",
            {"saves": [self._slot_to_dict(slot) for slot in slots]},
        )

    def _parse_slot(self, data: object) -> SaveSlot | None:
        if not isinstance(data, dict):
            return None

        save_id = data.get("id")
        name = data.get("name")
        created_at = data.get("created_at")
        updated_at = data.get("updated_at")
        game_state_data = data.get("game_state")

        if not isinstance(save_id, str) or not save_id:
            return None
        if not isinstance(name, str) or not name.strip():
            name = self._default_name(updated_at if isinstance(updated_at, str) else self._now())
        if not isinstance(created_at, str) or not isinstance(updated_at, str):
            return None
        if not isinstance(game_state_data, dict):
            return None

        game_state = GameState.from_dict(game_state_data)
        if game_state is None:
            return None

        return SaveSlot(
            save_id=save_id,
            name=name.strip()[:24],
            created_at=created_at,
            updated_at=updated_at,
            game_state=game_state,
        )

    def _migrate_legacy_save(self, raw_data: object) -> SaveSlot | None:
        if not isinstance(raw_data, dict) or not raw_data.get("has_save"):
            return None
        game_state_data = raw_data.get("game_state")
        if not isinstance(game_state_data, dict):
            return None
        game_state = GameState.from_dict(game_state_data)
        if game_state is None:
            return None
        now = self._now()
        return SaveSlot(uuid4().hex, self._default_name(now), now, now, game_state)

    def _slot_to_dict(self, slot: SaveSlot) -> dict[str, object]:
        return {
            "id": slot.save_id,
            "name": slot.name,
            "created_at": slot.created_at,
            "updated_at": slot.updated_at,
            "game_state": slot.game_state.to_dict(),
        }

    def _now(self) -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _default_name(self, timestamp: str) -> str:
        return f"\u5b58\u6863 {timestamp}"
