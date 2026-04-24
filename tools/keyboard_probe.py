from __future__ import annotations

import pygame


WINDOW_SIZE = (760, 360)
BACKGROUND = (20, 20, 20)
TEXT = (240, 240, 240)


def main() -> None:
    pygame.init()
    pygame.key.start_text_input()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Keyboard Probe")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 28)

    lines = [
        "Keyboard Probe",
        "Press arrows, W/A/S/D, numbers, Enter, mouse.",
        "Waiting for input...",
    ]
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                key = getattr(event, "key", None)
                scancode = getattr(event, "scancode", None)
                unicode_text = getattr(event, "unicode", "")
                key_name = pygame.key.name(key) if isinstance(key, int) else "None"
                lines.insert(
                    2,
                    f"KEYDOWN key={key} ({key_name}) scancode={scancode} unicode={unicode_text!r}",
                )
            elif event.type == pygame.KEYUP:
                key = getattr(event, "key", None)
                key_name = pygame.key.name(key) if isinstance(key, int) else "None"
                lines.insert(2, f"KEYUP key={key} ({key_name})")
            elif event.type == pygame.TEXTINPUT:
                lines.insert(2, f"TEXTINPUT text={event.text!r}")
            elif event.type == pygame.MOUSEBUTTONDOWN:
                lines.insert(2, f"MOUSEBUTTONDOWN pos={event.pos} button={event.button}")

        keys = pygame.key.get_pressed()
        pressed = []
        watched = [
            ("W", pygame.K_w),
            ("A", pygame.K_a),
            ("S", pygame.K_s),
            ("D", pygame.K_d),
            ("UP", pygame.K_UP),
            ("DOWN", pygame.K_DOWN),
            ("LEFT", pygame.K_LEFT),
            ("RIGHT", pygame.K_RIGHT),
        ]
        for label, key_code in watched:
            if keys[key_code]:
                pressed.append(label)

        screen.fill(BACKGROUND)
        status = "get_pressed: " + (", ".join(pressed) if pressed else "(none)")
        draw_line(screen, font, status, 20, 20)
        for index, line in enumerate(lines[:11]):
            draw_line(screen, font, line, 20, 60 + index * 28)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


def draw_line(screen: pygame.Surface, font: pygame.font.Font, text: str, x: int, y: int) -> None:
    surface = font.render(text, True, TEXT)
    screen.blit(surface, (x, y))


if __name__ == "__main__":
    main()
