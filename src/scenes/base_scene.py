from __future__ import annotations

import pygame


class BaseScene:
    """Shared interface for all scenes."""

    def __init__(self, app) -> None:
        self.app = app

    def handle_event(self, event: pygame.event.Event) -> bool:
        return True

    def update(self, delta_ms: int) -> None:
        _ = delta_ms

    def render(self, screen: pygame.Surface) -> None:
        raise NotImplementedError
