from __future__ import annotations

from src.core import system_keys


def pressed_up() -> bool:
    return system_keys.any_pressed(system_keys.VK_UP, system_keys.VK_W)


def pressed_down() -> bool:
    return system_keys.any_pressed(system_keys.VK_DOWN, system_keys.VK_S)


def pressed_left() -> bool:
    return system_keys.any_pressed(system_keys.VK_LEFT, system_keys.VK_A)


def pressed_right() -> bool:
    return system_keys.any_pressed(system_keys.VK_RIGHT, system_keys.VK_D)


def pressed_direction() -> tuple[int, int] | None:
    from src.constants import DOWN, LEFT, RIGHT, UP

    if pressed_up():
        return UP
    if pressed_down():
        return DOWN
    if pressed_left():
        return LEFT
    if pressed_right():
        return RIGHT
    return None
