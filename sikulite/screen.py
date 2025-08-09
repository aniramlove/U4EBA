from __future__ import annotations

from typing import Optional, Tuple, Dict

import mss
import numpy as np
import cv2


class ScreenCapturer:
    def __init__(self) -> None:
        self._mss = mss.mss()

    def get_full_region(self) -> Tuple[int, int, int, int]:
        mon = self._mss.monitors[0]  # bounding box across monitors
        return mon["left"], mon["top"], mon["width"], mon["height"]

    def grab(self, region: Optional[Tuple[int, int, int, int]] = None) -> np.ndarray:
        if region is None:
            left, top, width, height = self.get_full_region()
        else:
            left, top, width, height = region
        bbox: Dict[str, int] = {"left": int(left), "top": int(top), "width": int(width), "height": int(height)}
        shot = self._mss.grab(bbox)
        img = np.array(shot)  # BGRA
        img_bgr = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        return img_bgr

    def close(self) -> None:
        try:
            self._mss.close()
        except Exception:
            pass