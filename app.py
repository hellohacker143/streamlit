import streamlit as st
import cv2
from PIL import Image

# Streamlit configuration
st.set_page_config(page_title="OpenCV Webcam Example")
st.header("OpenCV Webcam Example with Streamlit")

# Create an empty container to display the webcam feed
frame_placeholder = st.empty()

# Open the webcam
cap = cv2.VideoCapture(0)

# Check if the webcam opened successfully
if not cap.isOpened():
    st.error("Unable to access the camera")

# Display video frames in Streamlit
while True:
    ret, frame = cap.read()  # Capture frame-by-frame

    if not ret:
        st.error("Failed to grab frame")
        break

    # Convert frame to RGB (OpenCV uses BGR by default)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Display the frame using Streamlit
    img = Image.fromarray(frame_rgb)
    frame_placeholder.image(img, channels="RGB", use_column_width=True)

    # Stop the video feed with the 'Stop Webcam' button
    if st.button('Stop Webcam'):
        break

# Release the webcam when done
cap.release()
