from __future__ import annotations

import pygame


class InputDebug:
    """Stores the latest key event for on-screen diagnostics."""

    def __init__(self) -> None:
        self.enabled = False
        self.last_key_text = "No key event yet"

    def record_system_key(self, action: str) -> None:
        self.last_key_text = f"Windows KEYDOWN action={action}"

    def record(self, event: pygame.event.Event) -> None:
        if event.type == pygame.TEXTINPUT:
            self.last_key_text = f"TEXTINPUT text={event.text!r}"
            return

        if event.type != pygame.KEYDOWN:
            return

        key = getattr(event, "key", None)
        scancode = getattr(event, "scancode", None)
        unicode_text = getattr(event, "unicode", "")
        key_name = pygame.key.name(key) if isinstance(key, int) else "None"
        self.last_key_text = (
            f"key={key} ({key_name})  scancode={scancode}  unicode={unicode_text!r}"
        )
