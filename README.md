# SikuliLite (Python)

A lightweight, scriptable desktop automation tool inspired by SikuliX. It performs actions based on image matching: find an image on screen, click/type/hotkey, wait, and more.

## Features
- Image-based matching using OpenCV (multi-scale search)
- Mouse/keyboard automation with `pynput`
- Screen capture via `mss`
- YAML scripts to define flows
- Optional debug visualization and confidence logging

## Install
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run
```bash
python -m sikulite run scripts/example.yaml --templates templates --debug
```

- Put UI snapshots under `templates/` (e.g., `ok_button.png`).
- Edit `scripts/example.yaml` to point to your images and actions.

## YAML Script Schema (quick)
```yaml
steps:
  - wait_for:
      image: ok_button.png
      timeout: 10        # seconds
      interval: 0.5      # seconds
      threshold: 0.9
      region: [x, y, w, h]  # optional crop
  - click:
      image: ok_button.png # or {x: 100, y: 200}
      threshold: 0.9
      offset: [dx, dy]
  - type_text:
      text: "Hello"
      interval: 0.03
  - hotkey:
      keys: ["ctrl", "s"]
  - sleep: 1.0
```

## Tips
- Use your OS screenshot tool to create clear templates at the same scale as your desktop. Store them in `templates/`.
- You can disable multi-scale search by setting `scale_min == scale_max == 1.0` in your script-level defaults.

## Disclaimer
Desktop automation can be disruptive. Test carefully on a non-critical workspace first.
