import cv2
import mediapipe as mp
import streamlit as st
import threading
from PIL import Image

# Initialize MediaPipe Hands for hand gesture recognition
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Streamlit camera input for hand gestures
st.set_page_config(page_title="Hand Gesture Scroll App")
st.header("Hand Gesture Scroll App")

# Webcam input using OpenCV and MediaPipe
stframe = st.empty()

def hand_gesture_scroll():
    # Open the webcam
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            continue

        # Flip the frame horizontally for a more natural appearance
        frame = cv2.flip(frame, 1)

        # Convert the frame to RGB (MediaPipe expects RGB)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        # Draw hand landmarks if any are detected
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Identify the position of the index and middle fingers (Landmark 8 and 12)
                index_finger = hand_landmarks.landmark[8]
                middle_finger = hand_landmarks.landmark[12]

                # Check if hand gesture is swipe up or down based on finger positions
                if index_finger.y < middle_finger.y:  # Swipe up gesture
                    st.markdown(
                        """
                        <script>
                        window.scrollBy(0, -100);
                        </script>
                        """,
                        unsafe_allow_html=True
                    )
                elif index_finger.y > middle_finger.y:  # Swipe down gesture
                    st.markdown(
                        """
                        <script>
                        window.scrollBy(0, 100);
                        </script>
                        """,
                        unsafe_allow_html=True
                    )

        # Show the frame in Streamlit
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        stframe.image(img, channels="RGB", use_column_width=True)

    cap.release()

# Start the webcam input in a separate thread
thread = threading.Thread(target=hand_gesture_scroll)
thread.daemon = True
thread.start()
