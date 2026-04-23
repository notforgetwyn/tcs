from __future__ import annotations

from dataclasses import dataclass, field

from src.constants import DOWN, LEFT, RIGHT, UP


Coordinate = tuple[int, int]


@dataclass
class Snake:
    """Maintains snake body positions and movement rules."""

    body: list[Coordinate] = field(
        default_factory=lambda: [(10, 10), (9, 10), (8, 10)]
    )
    direction: Coordinate = RIGHT
    pending_growth: int = 0

    def set_direction(self, new_direction: Coordinate) -> None:
        if new_direction not in {UP, DOWN, LEFT, RIGHT}:
            return

        if len(self.body) > 1:
            dx, dy = self.direction
            ndx, ndy = new_direction
            if dx + ndx == 0 and dy + ndy == 0:
                return

        self.direction = new_direction

    def move(self) -> None:
        head_x, head_y = self.body[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        self.body.insert(0, new_head)
        if self.pending_growth > 0:
            self.pending_growth -= 1
            return

        self.body.pop()

    def grow(self, amount: int = 1) -> None:
        if amount > 0:
            self.pending_growth += amount

    def get_head(self) -> Coordinate:
        return self.body[0]

    def collides_with_self(self) -> bool:
        return self.get_head() in self.body[1:]
