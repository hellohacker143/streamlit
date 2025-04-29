import streamlit as st

# Set the page title
st.set_page_config(page_title="Webcam Capture")

# Add a header
st.header("Capture an Image from Your Webcam")

# Use Streamlit's built-in camera input feature
image = st.camera_input("Take a picture")

# Check if an image is captured
if image is not None:
    # Display the captured image
    st.image(image)

    # Optionally, save the image to a file
    with open("captured_image.jpg", "wb") as f:
        f.write(image.getvalue())
    st.write("Captured image saved as 'captured_image.jpg'.")
