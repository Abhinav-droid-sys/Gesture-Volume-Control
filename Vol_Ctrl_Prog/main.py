import cv2
import numpy as np
import mediapipe as mp
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import math
from collections import deque

# MediaPipe Setup
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1)
mpDraw = mp.solutions.drawing_utils

# Volume Setup
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volRange = volume.GetVolumeRange()
minVol, maxVol = volRange[0], volRange[1]

# Webcam
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# Smoothing
smoothing_buffer = deque(maxlen=5)
minDist = 30
maxDist = 200

# Finger tip landmarks
fingertips = [4, 8, 12, 16, 20]

# Track mute state
muted = False

def fingers_up(lmList):
    fingers = []
    if not lmList:
        return fingers
    # Thumb
    fingers.append(1 if lmList[4][1] > lmList[3][1] else 0)
    # Fingers
    for tip in [8, 12, 16, 20]:
        fingers.append(1 if lmList[tip][2] < lmList[tip - 2][2] else 0)
    return fingers

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    lmList = []
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

            for id, lm in enumerate(handLms.landmark):
                h, w, _ = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append((id, cx, cy))

    if lmList:
        # Detect number of fingers up
        fingerStates = fingers_up(lmList)
        totalFingers = sum(fingerStates)

        if totalFingers == 0:
            volume.SetMute(1, None)
            muted = True
        elif totalFingers == 5:
            volume.SetMute(0, None)
            muted = False

        # Get thumb and index tip
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        length = math.hypot(x2 - x1, y2 - y1)

        # Clamp and Smooth
        clamped_length = max(min(length, maxDist), minDist)
        smoothing_buffer.append(clamped_length)
        avg_length = sum(smoothing_buffer) / len(smoothing_buffer)

        # Interpolate to volume
        vol = np.interp(avg_length, [minDist, maxDist], [minVol, maxVol])
        vol_percent = np.interp(avg_length, [minDist, maxDist], [0, 100])

        # Set volume if not muted
        if not muted:
            volume.SetMasterVolumeLevel(vol, None)

        # Visuals
        barHeight = np.interp(avg_length, [minDist, maxDist], [400, 150])
        color = (0, 255, 0) if not muted else (0, 0, 255)

        # Volume Bar
        cv2.rectangle(img, (50, 150), (85, 400), (200, 200, 200), 2)
        cv2.rectangle(img, (50, int(barHeight)), (85, 400), color, cv2.FILLED)
        cv2.putText(img, f'{int(vol_percent)}%', (40, 430), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

        # Status
        status = "Muted" if muted else "Volume Active"
        cv2.putText(img, status, (200, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

        # Draw connection line and circles
        cv2.line(img, (x1, y1), (x2, y2), color, 2)
        cv2.circle(img, (x1, y1), 8, color, cv2.FILLED)
        cv2.circle(img, (x2, y2), 8, color, cv2.FILLED)

    else:
        muted = False

    cv2.imshow("Volume Control with Mute", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
