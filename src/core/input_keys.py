from __future__ import annotations

import pygame


def is_up(event: pygame.event.Event) -> bool:
    return _matches(event, key_codes={pygame.K_UP, pygame.K_w}, scan_codes={pygame.KSCAN_W}, chars={"w"})


def is_down(event: pygame.event.Event) -> bool:
    return _matches(event, key_codes={pygame.K_DOWN, pygame.K_s}, scan_codes={pygame.KSCAN_S}, chars={"s"})


def is_left(event: pygame.event.Event) -> bool:
    return _matches(event, key_codes={pygame.K_LEFT, pygame.K_a}, scan_codes={pygame.KSCAN_A}, chars={"a"})


def is_right(event: pygame.event.Event) -> bool:
    return _matches(event, key_codes={pygame.K_RIGHT, pygame.K_d}, scan_codes={pygame.KSCAN_D}, chars={"d"})


def _matches(
    event: pygame.event.Event,
    *,
    key_codes: set[int],
    scan_codes: set[int],
    chars: set[str],
) -> bool:
    key = getattr(event, "key", None)
    if key in key_codes:
        return True

    scancode = getattr(event, "scancode", None)
    if scancode in scan_codes:
        return True

    text = getattr(event, "unicode", "")
    return isinstance(text, str) and text.lower() in chars
