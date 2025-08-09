from __future__ import annotations

import os
import time
from dataclasses import dataclass
from typing import Any, Dict, Optional, Tuple

import yaml

from .screen import ScreenCapturer
from .finder import TemplateMatcher
from .actions import MouseActions, KeyboardActions
from .utils import console


@dataclass
class Defaults:
    threshold: float = 0.9
    scale_min: float = 1.0
    scale_max: float = 1.0
    num_scales: int = 10
    interval: float = 0.5
    region: Optional[Tuple[int, int, int, int]] = None


class ScriptRunner:
    def __init__(
        self,
        templates_dir: str,
        debug: bool = False,
        dry_run: bool = False,
    ) -> None:
        self.templates_dir = templates_dir
        self.debug = debug
        self.dry_run = dry_run
        self.capturer = ScreenCapturer()
        self.matcher = TemplateMatcher()
        self.mouse = MouseActions(dry_run=dry_run)
        self.keyboard = KeyboardActions(dry_run=dry_run)

    def _resolve_template(self, name: str) -> str:
        path = name
        if not os.path.isabs(path):
            path = os.path.join(self.templates_dir, name)
        return path

    def _grab(self, region: Optional[Tuple[int, int, int, int]] = None):
        return self.capturer.grab(region)

    def _wait_for(
        self,
        image: str,
        timeout: float,
        interval: float,
        threshold: float,
        scale_min: float,
        scale_max: float,
        num_scales: int,
        region: Optional[Tuple[int, int, int, int]] = None,
    ) -> Optional[Dict[str, Any]]:
        from .utils import load_image_bgr

        deadline = time.time() + timeout
        template_path = self._resolve_template(image)
        template_bgr = load_image_bgr(template_path)

        while time.time() < deadline:
            shot_bgr = self._grab(region)
            result = self.matcher.find_best(
                shot_bgr, template_bgr, threshold, scale_min, scale_max, num_scales
            )
            if result.found:
                if self.debug:
                    console.log(f"Found '{image}' with score={result.score:.3f} at {result.top_left} size={result.size}")
                # adjust to absolute if region was used
                offset_x = region[0] if region else 0
                offset_y = region[1] if region else 0
                cx, cy = result.center
                return {
                    "center": (cx + offset_x, cy + offset_y),
                    "top_left": (result.top_left[0] + offset_x, result.top_left[1] + offset_y),
                    "size": result.size,
                    "score": result.score,
                }
            time.sleep(max(0.01, interval))
        return None

    def run_script(self, path: str) -> None:
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}

        defaults_data: Dict[str, Any] = data.get("defaults", {})
        defaults = Defaults(
            threshold=float(defaults_data.get("threshold", 0.9)),
            scale_min=float(defaults_data.get("scale_min", 1.0)),
            scale_max=float(defaults_data.get("scale_max", 1.0)),
            num_scales=int(defaults_data.get("num_scales", 10)),
            interval=float(defaults_data.get("interval", 0.5)),
            region=tuple(defaults_data.get("region")) if defaults_data.get("region") else None,
        )

        steps = data.get("steps", [])
        for idx, step in enumerate(steps):
            if not isinstance(step, dict) or len(step) != 1:
                raise ValueError(f"Invalid step at index {idx}: {step}")
            action, params = next(iter(step.items()))
            params = params or {}

            if action == "wait_for":
                image = params["image"]
                timeout = float(params.get("timeout", 10))
                interval = float(params.get("interval", defaults.interval))
                threshold = float(params.get("threshold", defaults.threshold))
                scale_min = float(params.get("scale_min", defaults.scale_min))
                scale_max = float(params.get("scale_max", defaults.scale_max))
                num_scales = int(params.get("num_scales", defaults.num_scales))
                region = params.get("region", defaults.region)
                if region is not None:
                    region = tuple(region)  # type: ignore
                hit = self._wait_for(
                    image=image,
                    timeout=timeout,
                    interval=interval,
                    threshold=threshold,
                    scale_min=scale_min,
                    scale_max=scale_max,
                    num_scales=num_scales,
                    region=region,  # type: ignore
                )
                if hit is None:
                    raise TimeoutError(f"Timeout waiting for image: {image}")
                last_point = hit["center"]
                last_box = (hit["top_left"], hit["size"])  # for potential future use
                if self.debug:
                    console.log(f"wait_for -> center={last_point}")
                # cache last found position for subsequent steps
                params["_last_center"] = last_point
                params["_last_box"] = last_box

            elif action in ("click", "move"):
                point = None
                if "image" in params:
                    # find once without waiting
                    image = params["image"]
                    threshold = float(params.get("threshold", defaults.threshold))
                    scale_min = float(params.get("scale_min", defaults.scale_min))
                    scale_max = float(params.get("scale_max", defaults.scale_max))
                    num_scales = int(params.get("num_scales", defaults.num_scales))
                    region = params.get("region", defaults.region)
                    if region is not None:
                        region = tuple(region)  # type: ignore
                    hit = self._wait_for(
                        image=image,
                        timeout=float(params.get("timeout", 0.1)),
                        interval=float(params.get("interval", 0.05)),
                        threshold=threshold,
                        scale_min=scale_min,
                        scale_max=scale_max,
                        num_scales=num_scales,
                        region=region,  # type: ignore
                    )
                    if hit is None:
                        raise RuntimeError(f"Image not found for {action}: {image}")
                    point = hit["center"]
                elif "x" in params and "y" in params:
                    point = (int(params["x"]), int(params["y"]))
                else:
                    raise ValueError(f"{action} requires either 'image' or 'x'/'y'")

                offset = params.get("offset")
                if offset:
                    point = (int(point[0] + offset[0]), int(point[1] + offset[1]))

                if action == "move":
                    if self.debug:
                        console.log(f"move -> {point}")
                    self.mouse.move_to(*point)
                else:
                    button = params.get("button", "left")
                    clicks = int(params.get("clicks", 1))
                    if self.debug:
                        console.log(f"click -> {point}, button={button}, clicks={clicks}")
                    self.mouse.click(*point, button=button, clicks=clicks)

            elif action == "type_text":
                text = params.get("text", "")
                interval = float(params.get("interval", 0.02))
                if self.debug:
                    console.log(f"type_text -> '{text}'")
                self.keyboard.type_text(text, interval=interval)

            elif action == "hotkey":
                keys = params.get("keys", [])
                if not isinstance(keys, list) or not keys:
                    raise ValueError("hotkey requires a non-empty list 'keys'")
                if self.debug:
                    console.log(f"hotkey -> {keys}")
                self.keyboard.hotkey(keys)

            elif action == "sleep":
                secs = float(params)
                if self.debug:
                    console.log(f"sleep -> {secs}s")
                time.sleep(max(0.0, secs))

            else:
                raise ValueError(f"Unknown action: {action}")

    def close(self) -> None:
        self.capturer.close()