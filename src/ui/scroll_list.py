from __future__ import annotations

from collections.abc import Sequence
from typing import TypeVar

T = TypeVar("T")


class ScrollList:
    """Selection and scroll state for a vertical list."""

    def __init__(self, max_visible_items: int) -> None:
        self.max_visible_items = max_visible_items
        self.item_count = 0
        self.extra_selectable_count = 0
        self.selected_index = 0
        self.scroll_offset = 0

    def configure(self, item_count: int, *, extra_selectable_count: int = 0) -> None:
        self.item_count = max(0, item_count)
        self.extra_selectable_count = max(0, extra_selectable_count)
        self.selected_index = min(self.selected_index, self.last_selectable_index())
        self.scroll_offset = min(self.scroll_offset, self.max_scroll_offset())
        self.sync_to_selection()

    def move_selection(self, step: int) -> int:
        total = self.item_count + self.extra_selectable_count
        if total <= 0:
            self.selected_index = 0
            self.scroll_offset = 0
            return self.selected_index

        self.selected_index = (self.selected_index + step) % total
        self.sync_to_selection()
        return self.selected_index

    def scroll(self, step: int) -> int:
        if self.item_count <= self.max_visible_items:
            return self.selected_index

        self.scroll_offset = max(0, min(self.max_scroll_offset(), self.scroll_offset + step))

        if self.selected_index < self.scroll_offset:
            self.selected_index = self.scroll_offset
        elif self.selected_index >= self.scroll_offset + self.max_visible_items:
            self.selected_index = self.scroll_offset + self.max_visible_items - 1
        return self.selected_index

    def visible_items(self, items: Sequence[T]) -> list[tuple[int, T]]:
        end = min(self.scroll_offset + self.max_visible_items, len(items))
        return [(index, items[index]) for index in range(self.scroll_offset, end)]

    def scroll_status(self) -> tuple[int, int, int]:
        if self.item_count == 0:
            return 0, 0, 0
        start = self.scroll_offset + 1
        end = min(self.scroll_offset + self.max_visible_items, self.item_count)
        return start, end, self.item_count

    def sync_to_selection(self) -> None:
        if self.selected_index >= self.item_count:
            return
        if self.selected_index < self.scroll_offset:
            self.scroll_offset = self.selected_index
        elif self.selected_index >= self.scroll_offset + self.max_visible_items:
            self.scroll_offset = self.selected_index - self.max_visible_items + 1

    def max_scroll_offset(self) -> int:
        return max(0, self.item_count - self.max_visible_items)

    def last_selectable_index(self) -> int:
        total = self.item_count + self.extra_selectable_count
        return max(0, total - 1)
