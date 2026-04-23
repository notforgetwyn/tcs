from __future__ import annotations

from dataclasses import dataclass

from src.constants import DOWN, GRID_HEIGHT, GRID_WIDTH, LEFT, RIGHT, UP
from src.core.settings_service import (
    DEFAULT_MOVE_INTERVAL_MS,
    MAX_MOVE_INTERVAL_MS,
    MIN_MOVE_INTERVAL_MS,
)


Coordinate = tuple[int, int]
VALID_DIRECTIONS = {UP, DOWN, LEFT, RIGHT}


@dataclass
class GameState:
    snake_body: list[Coordinate]
    direction: Coordinate
    food_position: Coordinate
    score: int
    move_interval_ms: int
    pending_growth: int = 0

    def to_dict(self) -> dict[str, object]:
        return {
            "snake_body": [list(position) for position in self.snake_body],
            "direction": list(self.direction),
            "food_position": list(self.food_position),
            "score": self.score,
            "move_interval_ms": self.move_interval_ms,
            "pending_growth": self.pending_growth,
        }

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> GameState | None:
        snake_body = cls._parse_positions(data.get("snake_body"))
        direction = cls._parse_position(data.get("direction"))
        food_position = cls._parse_position(data.get("food_position"))
        score = data.get("score")
        move_interval_ms = data.get("move_interval_ms")
        pending_growth = data.get("pending_growth", 0)

        if not snake_body or direction not in VALID_DIRECTIONS or food_position is None:
            return None
        if not isinstance(score, int) or score < 0:
            return None
        if not isinstance(move_interval_ms, int):
            move_interval_ms = DEFAULT_MOVE_INTERVAL_MS
        move_interval_ms = max(MIN_MOVE_INTERVAL_MS, min(MAX_MOVE_INTERVAL_MS, move_interval_ms))
        if not isinstance(pending_growth, int) or pending_growth < 0:
            pending_growth = 0
        if len(set(snake_body)) != len(snake_body):
            return None
        if food_position in snake_body:
            return None

        return cls(
            snake_body=snake_body,
            direction=direction,
            food_position=food_position,
            score=score,
            move_interval_ms=move_interval_ms,
            pending_growth=pending_growth,
        )

    @staticmethod
    def _parse_positions(value: object) -> list[Coordinate] | None:
        if not isinstance(value, list) or not value:
            return None

        positions: list[Coordinate] = []
        for item in value:
            position = GameState._parse_position(item)
            if position is None:
                return None
            positions.append(position)
        return positions

    @staticmethod
    def _parse_position(value: object) -> Coordinate | None:
        if not isinstance(value, (list, tuple)) or len(value) != 2:
            return None

        x, y = value
        if not isinstance(x, int) or not isinstance(y, int):
            return None
        if not (0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT):
            return None
        return (x, y)
