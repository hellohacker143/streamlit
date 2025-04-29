import streamlit as st
import cv2
import mediapipe as mp
from PIL import Image

# Set up MediaPipe for hand tracking
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Set up Streamlit page config
st.set_page_config(page_title="Webcam Capture with Hand Gesture Scrolling")
st.header("Capture Image and Control Scrolling with Hand Gestures")

# Create an empty container to display the webcam feed
stframe = st.empty()

# Start webcam feed
cap = cv2.VideoCapture(0)

def detect_gesture(frame):
    # Convert the frame to RGB (MediaPipe expects RGB)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    # Gesture detection logic
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Identify the position of the index and middle fingers (Landmark 8 and 12)
            index_finger = hand_landmarks.landmark[8]
            middle_finger = hand_landmarks.landmark[12]

            # If index finger is above middle finger, it's a swipe-up gesture
            if index_finger.y < middle_finger.y:
                st.markdown(
                    """
                    <script>
                    window.scrollBy(0, -100);  // Scroll up
                    </script>
                    """,
                    unsafe_allow_html=True
                )

            # If index finger is below middle finger, it's a swipe-down gesture
            elif index_finger.y > middle_finger.y:
                st.markdown(
                    """
                    <script>
                    window.scrollBy(0, 100);  // Scroll down
                    </script>
                    """,
                    unsafe_allow_html=True
                )

# Display webcam feed and process frames
while True:
    ret, frame = cap.read()

    if not ret:
        break

    # Flip the frame horizontally for a more natural appearance
    frame = cv2.flip(frame, 1)

    # Detect gestures
    detect_gesture(frame)

    # Convert frame to RGB for Streamlit display
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(frame_rgb)
    
    # Show the frame in Streamlit
    stframe.image(img, channels="RGB", use_column_width=True)

    # Stop the webcam feed with the "Stop Webcam" button
    if st.button("Stop Webcam"):
        break

# Release the webcam after use
cap.release()
