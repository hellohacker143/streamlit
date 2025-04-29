import streamlit as st

# Set the page title
st.set_page_config(page_title="Webcam Capture")

# Add a header to the app
st.header("Capture an Image from Your Webcam")

# Open the webcam and capture an image
camera_input = st.camera_input("Take a picture")

# Check if the camera input is not None (i.e., an image is captured)
if camera_input is not None:
    # Display the captured image
    st.image(camera_input)

    # You can also save the captured image if you wish
    with open("captured_image.jpg", "wb") as f:
        f.write(camera_input.getvalue())
    st.write("Captured image saved as 'captured_image.jpg'.")
