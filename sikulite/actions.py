from __future__ import annotations

import time
from typing import Iterable, List, Tuple, Union

from pynput.mouse import Controller as MouseController, Button
from pynput.keyboard import Controller as KeyboardController, Key

from .utils import parse_key_sequence


class MouseActions:
    def __init__(self, dry_run: bool = False) -> None:
        self.mouse = MouseController()
        self.dry_run = dry_run

    def move_to(self, x: int, y: int) -> None:
        if self.dry_run:
            return
        self.mouse.position = (int(x), int(y))

    def click(self, x: int, y: int, button: str = "left", clicks: int = 1) -> None:
        if self.dry_run:
            return
        self.move_to(x, y)
        btn = {"left": Button.left, "right": Button.right, "middle": Button.middle}.get(button, Button.left)
        for _ in range(max(1, int(clicks))):
            self.mouse.click(btn)
            time.sleep(0.05)


class KeyboardActions:
    def __init__(self, dry_run: bool = False) -> None:
        self.keyboard = KeyboardController()
        self.dry_run = dry_run

    def type_text(self, text: str, interval: float = 0.02) -> None:
        if self.dry_run:
            return
        for ch in text:
            self.keyboard.type(ch)
            if interval > 0:
                time.sleep(interval)

    def hotkey(self, keys: Iterable[str]) -> None:
        if self.dry_run:
            return
        seq: List[Union[Key, str]] = parse_key_sequence(keys)
        # Press in order, release in reverse
        for k in seq:
            self.keyboard.press(k)
        for k in reversed(seq):
            self.keyboard.release(k)
            time.sleep(0.01)