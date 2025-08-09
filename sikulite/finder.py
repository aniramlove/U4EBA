from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple

import cv2
import numpy as np

from .utils import to_gray


@dataclass
class MatchResult:
    found: bool
    score: float
    top_left: Tuple[int, int]
    size: Tuple[int, int]

    @property
    def center(self) -> Tuple[int, int]:
        x, y = self.top_left
        w, h = self.size
        return int(x + w / 2), int(y + h / 2)


class TemplateMatcher:
    def __init__(self, method: int = cv2.TM_CCOEFF_NORMED) -> None:
        self.method = method

    def find_best(
        self,
        haystack_bgr: np.ndarray,
        needle_bgr: np.ndarray,
        threshold: float = 0.9,
        scale_min: float = 1.0,
        scale_max: float = 1.0,
        num_scales: int = 10,
    ) -> MatchResult:
        haystack_gray = to_gray(haystack_bgr)
        needle_gray_orig = to_gray(needle_bgr)

        if scale_min <= 0 or scale_max <= 0:
            raise ValueError("scale_min and scale_max must be > 0")
        if scale_max < scale_min:
            scale_min, scale_max = scale_max, scale_min

        best_score = -1.0
        best_loc = (0, 0)
        best_size = (0, 0)

        if abs(scale_max - scale_min) < 1e-6:
            scales = [scale_min]
        else:
            scales = np.linspace(scale_min, scale_max, num_scales)

        for scale in scales:
            h, w = needle_gray_orig.shape[:2]
            new_w = max(1, int(w * scale))
            new_h = max(1, int(h * scale))
            resized = cv2.resize(
                needle_gray_orig,
                (new_w, new_h),
                interpolation=cv2.INTER_AREA if scale < 1.0 else cv2.INTER_CUBIC,
            )
            if haystack_gray.shape[0] < new_h or haystack_gray.shape[1] < new_w:
                continue

            result = cv2.matchTemplate(haystack_gray, resized, self.method)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

            score = max_val
            loc = max_loc
            if score > best_score:
                best_score = score
                best_loc = loc
                best_size = (new_w, new_h)

        return MatchResult(
            found=best_score >= threshold,
            score=float(best_score),
            top_left=(int(best_loc[0]), int(best_loc[1])),
            size=(int(best_size[0]), int(best_size[1])),
        )