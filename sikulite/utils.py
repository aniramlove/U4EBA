from __future__ import annotations

from typing import Iterable, List, Tuple, Union

from rich.console import Console
from pynput.keyboard import Key
import cv2
import numpy as np

console = Console()


def load_image_bgr(path: str) -> np.ndarray:
    image = cv2.imread(path, cv2.IMREAD_COLOR)
    if image is None:
        raise FileNotFoundError(f"Failed to load image: {path}")
    return image


def to_gray(image_bgr: np.ndarray) -> np.ndarray:
    return cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)


def parse_key_token(token: str) -> Union[Key, str]:
    token_lower = token.lower()
    special = {
        "ctrl": Key.ctrl,
        "control": Key.ctrl,
        "alt": Key.alt,
        "shift": Key.shift,
        "cmd": Key.cmd,
        "win": Key.cmd,
        "meta": Key.cmd,
        "enter": Key.enter,
        "return": Key.enter,
        "esc": Key.esc,
        "escape": Key.esc,
        "tab": Key.tab,
        "space": Key.space,
        "backspace": Key.backspace,
        "delete": Key.delete,
        "home": Key.home,
        "end": Key.end,
        "page_up": Key.page_up,
        "page-down": Key.page_down,
        "page_down": Key.page_down,
        "up": Key.up,
        "down": Key.down,
        "left": Key.left,
        "right": Key.right,
    }
    # Function keys
    for i in range(1, 25):
        if token_lower == f"f{i}":
            return getattr(Key, f"f{i}")

    if token_lower in special:
        return special[token_lower]

    if len(token) == 1:
        return token

    # fallback: send as literal characters
    return token


def parse_key_sequence(tokens: Iterable[str]) -> List[Union[Key, str]]:
    return [parse_key_token(t) for t in tokens]


def clamp(value: float, min_value: float, max_value: float) -> float:
    return max(min_value, min(max_value, value))


def rect_center(x: int, y: int, w: int, h: int) -> Tuple[int, int]:
    cx = int(x + w / 2)
    cy = int(y + h / 2)
    return cx, cy