# Hand Gesture Control

## Overview

This project enables computer control using hand gestures detected by a webcam. Leveraging the MediaPipe Hands library, the system recognizes hand landmarks and executes actions based on gestures.

## Features

- **Left-click Gesture:** Thumb and index finger close proximity.
- **Right-click Gesture:** Extended pinky finger with a cooldown period.
- **Scroll Gesture:** Both index and middle fingers extended, with an option to enable/disable scrolling.
- **Hand Tracking:** Detects hand movements and maps them to control the mouse.

## Setup

### Requirements

- Python 3.6 or later
- OpenCV (`pip install opencv-python`)
- Mediapipe (`pip install mediapipe`)
- Mouse (`pip install mouse`)
- Screeninfo (`pip install screeninfo`)

### Installation

1. Install the required libraries:
   ```bash
   pip install opencv-python mediapipe mouse screeninfo
   ```
2. Clone the repository:

```bash
git clone https://github.com/your-username/hand-gesture-control.git
cd hand-gesture-control
```
Run the main script:
```bash
python main.py
```
## Usage
1. Left-click Gesture: Thumb and index finger close together. 
2. Right-click Gesture: Extend pinky finger with a cooldown period.
3. Scroll Gesture: Extend both index and middle fingers.
4. Hand Tracking: Move your hand to control the mouse pointer.
## Additional Options
- Press 's' to toggle scrolling on/off.
- Press 'q' to exit the application.
## Notes
Adjust gesture thresholds and cooldown periods in the script as needed.
Ensure proper lighting and hand visibility for accurate detection from webcam.

## License

This project is licensed under the MIT License.

### Third-Party Libraries and Tools

This project utilizes the following third-party libraries and tools, each subject to its respective license:

- [OpenCV](https://opencv.org/) - BSD License (3-clause)
- [MediaPipe](https://mediapipe.dev/) - Apache License 2.0
- [Mouse](https://github.com/boppreh/mouse) - MIT License
- [Screeninfo](https://github.com/rr-/screeninfo) - MIT License


