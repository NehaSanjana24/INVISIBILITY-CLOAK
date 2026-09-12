# Invisibility Cloak

A real-time Harry Potter-style invisibility cloak effect built with Python, OpenCV, and NumPy.

The app captures a clean background, detects a selected cloak color, and replaces matching pixels with the corresponding background pixels from the live webcam feed.

## Requirements

- Python 3.9 or newer
- A working webcam
- `opencv-python`
- `numpy`

## Installation

From the project directory, install the dependencies:

```powershell
pip install -r requirements.txt
```

## Run

Start the app with red as the default cloak color:

```powershell
python invisibility_cloak.py
```

Choose another target color:

```powershell
python invisibility_cloak.py --color green
python invisibility_cloak.py --color blue
```

When the window opens, step out of the camera view while the background is captured. Then wear or hold the selected-color cloak in front of the camera.

## Controls

| Key | Action |
| --- | --- |
| `r` | Capture the background again. Step out of frame first. |
| `s` | Save the current composited output as a timestamped PNG. |
| `m` | Toggle the binary mask debug view. |
| `q` | Quit and release the webcam. |

The window title is **Invisibility Cloak**.

## Tips

- Use bright, even lighting.
- Choose a cloak color that is not present elsewhere in the scene.
- Keep the camera still after capturing the background.
- Use `m` to check whether the entire cloak appears white in the mask view.
- Press `r` whenever the camera position, lighting, or background changes.

## Important limitation

This is color-based computer vision. It makes matching colored pixels invisible; it does not understand whether those pixels belong to cloth or a person. Avoid wearing the selected color anywhere else, and avoid backgrounds containing that color.
