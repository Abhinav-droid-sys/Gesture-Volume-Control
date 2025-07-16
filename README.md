# Gesture-Volume-Control
This project allows you to control your Windows system volume using hand gestures captured via webcam in real-time. By tracking the distance between your thumb and index finger, you can smoothly increase or decrease the volume. It also supports mute and unmute gestures using simple hand signs.

# 🔊 Hand Gesture-Based Volume Controller

Control your Windows system volume using real-time hand gestures via webcam! This project combines computer vision and system automation to allow intuitive, touchless control of audio levels using simple finger movements.

---

## 📽️ Demo

<img src="https://user-images.githubusercontent.com/000000/vol-ctrl-demo.gif" width="500"/>

> 👆 Pinch your fingers to increase or decrease volume  
> 👊 Close your hand (fist) to mute  
> ✋ Open your hand to unmute

---

## 🎯 Features

- 🤏 **Pinch Gesture**: Control volume by adjusting the distance between thumb and index finger
- ✊ **Fist Gesture**: Mute the system
- ✋ **Open Hand**: Unmute the system
- 📊 **Live Volume Bar**: Visual representation of volume level on-screen
- 🔁 **Smooth Transitions**: Uses moving average to reduce noise and jitter
- ⚡ **Real-time Processing**: Powered by MediaPipe and OpenCV

---

## 🛠️ Technologies Used

| Tool/Library | Description |
|--------------|-------------|
| [Python](https://www.python.org/) | Programming Language |
| [OpenCV](https://opencv.org/) | For webcam handling and image processing |
| [MediaPipe](https://google.github.io/mediapipe/) | Hand tracking and 21-point landmark detection |
| [PyCAW](https://github.com/AndreMiras/pycaw) | Python Core Audio Windows Library (system volume control) |
| NumPy | For distance interpolation and smoothing |
| Comtypes | COM interface wrapper required by PyCAW |

---

## 🧠 How It Works

1. Starts the webcam and detects a hand using MediaPipe.
2. Calculates the distance between the **thumb tip (landmark 4)** and **index finger tip (landmark 8)**.
3. Maps this distance to system volume range using interpolation.
4. Detects finger states:
   - **All fingers down (fist)** → Mute system
   - **All fingers up (open palm)** → Unmute system
5. Displays volume % and a live volume bar on the screen.
6. Volume changes smoothly with gesture thanks to a moving average filter.

---

## 🔧 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/Vol_Ctrl_prog.git
cd Vol_Ctrl_prog

pip install -r requirements.txt

Run main.py

