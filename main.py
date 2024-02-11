### Ron Niri 

import cv2
import mediapipe as mp
import numpy as np
import mouse
from screeninfo import get_monitors
import time

# Initialize MediaPipe Hands.
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.7)

# Initialize MediaPipe Drawing.
mp_drawing = mp.solutions.drawing_utils

# Open Webcam with the resolution 1920x1080 and a higher frame rate (e.g., 30 fps).
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
cap.set(cv2.CAP_PROP_FPS, 30)

# Get screen resolution
screen_width, screen_height = get_monitors()[0].width, get_monitors()[0].height

# Def Current gesture
current_gesture = "None" 
# Define the default dpi (0.5 means half the screen size)

dpi = 0.5

# Flag to keep track of the mouse click state
mouse_click_gesture = False

# Flag to enable/disable scrolling
enable_scrolling = True

# Cooldown period for right-click (in seconds)
right_click_cooldown = 2.0
last_right_click_time = time.time()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue

    # Flip the image horizontally for a selfie-view display.
    frame = cv2.flip(frame, 1)

    # Convert the BGR image to RGB.
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the image and find hand landmarks.
    results = hands.process(rgb_frame)

    # Calculate the rectangular region size based on dpi.
    region_width = int(screen_width * 1-dpi)
    region_height = screen_height
    region_start_x = int((screen_width - region_width) / 2)  # Centered position

    # Draw hand landmarks of each hand.
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Check if the thumb and index finger tips are close (left-click gesture).
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            thumb_index_distance = np.linalg.norm(np.array([thumb_tip.x, thumb_tip.y]) - np.array([index_finger_tip.x, index_finger_tip.y]))

            # Check if the pinky finger is extended (right-click gesture).
            pinky_extended = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_DIP].y

            # Check if the index and middle fingers are extended (scroll gesture).
            index_finger_extended = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP].y
            middle_finger_extended = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_DIP].y

            # Perform actions based on the hand gestures.
            if thumb_index_distance < 0.05:  # Adjust the threshold as needed
                if not mouse_click_gesture:
                    mouse.click('left')
                    mouse_click_gesture = True
                    current_gesture = "left-click" 
            else:
                mouse_click_gesture = False

            # Scroll up if both index and middle fingers are extended and scrolling is enabled.
            if index_finger_extended and middle_finger_extended and enable_scrolling:
                mouse.wheel(1)
                current_gesture = "Scroll Up"
                

            # Scroll down if both fingers are folded and scrolling is enabled.
            elif not index_finger_extended and not middle_finger_extended and enable_scrolling:
                mouse.wheel(-1)
                current_gesture = "Scroll Down"
                
            else:
                current_gesture = "No Gesture \ Pointer"

            # Right-click if the pinky finger is extended and cooldown period has passed.
            current_time = time.time()
            if pinky_extended and current_time - last_right_click_time > right_click_cooldown:
                mouse.click('right')
                last_right_click_time = current_time
                current_gesture = "Right Click"

            # Get the position of the tip of the index finger.
            x = int(index_finger_tip.x * frame.shape[1])
            y = int(index_finger_tip.y * frame.shape[0])

            # Map hand movement within the defined region to the entire screen.
            mapped_x = int((x - region_start_x) * (screen_width / region_width))
            mapped_y = int(y * (screen_height / region_height))
            
            mouse.move(mapped_x, mapped_y, absolute=True, duration=0)

    # Display the current gesture and scrolling toggle status in the top left corner.
    cv2.putText(frame, f"Gesture: {current_gesture}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, f"Scrolling: {'Enabled' if enable_scrolling else 'Disabled'}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    # Display the resulting frame.
    cv2.imshow(' mouse controling via hand gestures', frame)

    # Check for key presses
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('s'):
        enable_scrolling = not enable_scrolling

# Release the webcam and close windows.
cap.release()
cv2.destroyAllWindows()
