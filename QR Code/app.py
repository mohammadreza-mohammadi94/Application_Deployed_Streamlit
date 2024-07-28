import streamlit as st 
import numpy as np
import os 
import time 
from PIL import Image
import cv2
import qrcode

# Current timestamp
TIMESTR = time.strftime("%Y%m%d-%H%M%S")

# QR Code configuration
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)

def load_image(img_path):
    """
    Load an image from the specified file path.

    Parameters:
    img_path (str): The path to the image file.

    Returns:
    PIL.Image.Image: The loaded image.
    """
    return Image.open(img_path)

def generate_qr_code(text, save_path):
    """
    Generate a QR code from the provided text and save it to the specified path.

    Parameters:
    text (str): The text to encode in the QR code.
    save_path (str): The path to save the generated QR code image.

    Returns:
    PIL.Image.Image: The generated QR code image.
    """
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(fill_color='black', back_color='white')
    img.save(save_path)
    return load_image(save_path)

def decode_qr_code(image_file):
    """
    Decode a QR code from the provided image file.

    Parameters:
    image_file (UploadedFile): The uploaded image file containing the QR code.

    Returns:
    tuple: Decoded text, points of the QR code, and the straightened QR code image.
    """
    file_bytes = np.asarray(bytearray(image_file.read()), dtype=np.uint8)
    opencv_image = cv2.imdecode(file_bytes, 1)
    detector = cv2.QRCodeDetector()
    text, points, straight_qrcode = detector.detectAndDecode(opencv_image)
    return text, points, straight_qrcode, opencv_image

def main():
    """
    Main function to run the Streamlit QR Code application.
    """
    st.title("QR Code Application")
    menu = ["Home", "Decode QR", "About"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Home")
        with st.form(key='myqr_form'):
            raw_text = st.text_area("Enter text to generate QR code")
            submit_button = st.form_submit_button("Generate")

        if submit_button:
            col1, col2 = st.columns(2)

            with col1:
                img_filename = f'generate_image_{TIMESTR}.png'
                path_for_images = os.path.join('image_folder', img_filename)
                final_img = generate_qr_code(raw_text, path_for_images)
                st.image(final_img)

            with col2:
                st.info("Original Text")
                st.write(raw_text)

    elif choice == "Decode QR":
        st.subheader("Decode QR")
        image_file = st.file_uploader("Upload Image", type=['jpg', 'png', 'jpeg'])

        if image_file is not None:
            text, points, straight_qrcode, opencv_image = decode_qr_code(image_file)

            col1, col2 = st.columns(2)
            with col1:
                st.image(opencv_image, channels="BGR")

            with col2:
                st.info("Decoded QR Code")
                st.write("Text:", text)
                st.write("Points:", points)
                st.write("Straight QR Code:", straight_qrcode)

    elif choice == "About":
        st.subheader("About")
        st.write("This is a QR code generation and decoding application built with Streamlit.")

if __name__ == '__main__':
    main()
