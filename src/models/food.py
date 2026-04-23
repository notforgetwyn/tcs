from __future__ import annotations

import random
from dataclasses import dataclass

from src.constants import GRID_HEIGHT, GRID_WIDTH


Coordinate = tuple[int, int]


@dataclass
class Food:
    position: Coordinate = (0, 0)

    def respawn(self, occupied_positions: set[Coordinate]) -> None:
        available_positions = [
            (x, y)
            for x in range(GRID_WIDTH)
            for y in range(GRID_HEIGHT)
            if (x, y) not in occupied_positions
        ]

        if not available_positions:
            raise ValueError("No valid positions left to place food.")

        self.position = random.choice(available_positions)
