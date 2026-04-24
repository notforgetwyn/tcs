from __future__ import annotations

import tkinter as tk


MAX_LINES = 14


def main() -> None:
    root = tk.Tk()
    root.title("Tk Keyboard Probe")
    root.geometry("760x360")

    header = tk.Label(
        root,
        text="Tk Keyboard Probe - press W/A/S/D, arrows, numbers, Enter, mouse",
        anchor="w",
        font=("Consolas", 12),
    )
    header.pack(fill="x", padx=12, pady=(12, 4))

    output = tk.Text(root, height=16, font=("Consolas", 11))
    output.pack(fill="both", expand=True, padx=12, pady=8)
    output.insert("end", "Waiting for input...\n")

    def append(line: str) -> None:
        output.insert("1.0", line + "\n")
        current_lines = output.get("1.0", "end").splitlines()
        if len(current_lines) > MAX_LINES:
            output.delete(f"{MAX_LINES + 1}.0", "end")

    def on_key_press(event: tk.Event) -> None:
        append(
            "KeyPress "
            f"keysym={event.keysym!r} keycode={event.keycode} char={event.char!r} "
            f"state={event.state}"
        )

    def on_key_release(event: tk.Event) -> None:
        append(f"KeyRelease keysym={event.keysym!r} keycode={event.keycode} char={event.char!r}")

    def on_mouse(event: tk.Event) -> None:
        append(f"Mouse button={event.num} x={event.x} y={event.y}")

    root.bind("<KeyPress>", on_key_press)
    root.bind("<KeyRelease>", on_key_release)
    root.bind("<ButtonPress>", on_mouse)
    root.focus_force()
    root.mainloop()


if __name__ == "__main__":
    main()
