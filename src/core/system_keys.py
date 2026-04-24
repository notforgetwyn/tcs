from __future__ import annotations

import ctypes
import sys


VK_A = 0x41
VK_D = 0x44
VK_DOWN = 0x28
VK_ESCAPE = 0x1B
VK_F3 = 0x72
VK_LEFT = 0x25
VK_R = 0x52
VK_RETURN = 0x0D
VK_RIGHT = 0x27
VK_SPACE = 0x20
VK_S = 0x53
VK_UP = 0x26
VK_W = 0x57

_user32 = ctypes.windll.user32 if sys.platform == "win32" else None


def is_pressed(virtual_key: int) -> bool:
    if _user32 is None:
        return False
    return bool(_user32.GetAsyncKeyState(virtual_key) & 0x8000)


def any_pressed(*virtual_keys: int) -> bool:
    return any(is_pressed(virtual_key) for virtual_key in virtual_keys)


class KeyEdges:
    """Converts Windows key state into KEYDOWN-style one-shot actions."""

    def __init__(self) -> None:
        self._previous: dict[str, bool] = {}

    def just_pressed(self, action: str, *virtual_keys: int) -> bool:
        current = any_pressed(*virtual_keys)
        previous = self._previous.get(action, False)
        self._previous[action] = current
        return current and not previous
