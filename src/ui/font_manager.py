from __future__ import annotations

from functools import lru_cache

import pygame


PREFERRED_FONT_NAMES = [
    "microsoftyahei",
    "microsoftyaheiui",
    "simhei",
    "simsun",
    "notosanscjksc",
    "sourcehansanssc",
    "pingfangsc",
    "wenquanyizenheisharp",
]


@lru_cache(maxsize=32)
def get_font(size: int) -> pygame.font.Font:
    """Returns a readable font, preferring common Chinese fonts."""

    for font_name in PREFERRED_FONT_NAMES:
        font_path = pygame.font.match_font(font_name)
        if font_path:
            return pygame.font.Font(font_path, size)

    return pygame.font.Font(None, size)
