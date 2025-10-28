import streamlit as st
import cv2
import mediapipe as mp
import numpy as np

st.title("Streamlit Hand Gesture Control Demo")
run = st.checkbox('Start Camera')

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils
FRAME_WINDOW = st.image([])

def recognize_gesture(landmarks):
    # Custom logic for your gesture recognition. Example placeholder:
    return "Gesture Detected!"

if run:
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            st.error("Camera not found!")
            break
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)
        gesture = None
        if result.multi_hand_landmarks:
            for handLms in result.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)
                # You can analyze landmarks here for custom gestures
                gesture = recognize_gesture(handLms.landmark)
        if gesture:
            cv2.putText(frame, f"{gesture}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
        FRAME_WINDOW.image(frame)
    cap.release()
