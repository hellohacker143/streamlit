import streamlit as st
import cv2
import numpy as np
import mediapipe as mp

# MediaPipe and State
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

st.title("Hand Gesture Control Tool (Streamlit Demo)")
run = st.checkbox('Start Camera')

FRAME_WINDOW = st.image([])

def recognize_gesture(landmarks):
    # This is a placeholder for gesture recognition logic
    # You can train a simple classifier or use rules
    # Example: Thumb up = "Zoom In", Fist = "Zoom Out"
    # Return gesture as string ("zoom_in", "zoom_out", "play")
    return None

cap = None
if run:
    cap = cv2.VideoCapture(0)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            st.warning("Camera not detected.")
            break
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        res = hands.process(rgb)

        gesture = None
        if res.multi_hand_landmarks:
            for handlms in res.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, handlms, mp_hands.HAND_CONNECTIONS)
                # Get landmarks as list of (x, y)
                lm = [(lm.x, lm.y) for lm in handlms.landmark]
                gesture = recognize_gesture(lm)
        
        # Show detected gesture on screen
        if gesture:
            cv2.putText(frame, f"Gesture: {gesture}", (10,30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

        FRAME_WINDOW.image(frame)
        # Optionally send a request/command here if gesture is detected

    cap.release()
