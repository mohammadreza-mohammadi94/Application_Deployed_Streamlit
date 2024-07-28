import os
import exifread
from PIL import Image, ExifTags
import pandas as pd
import streamlit as st
from utils.file_utils import load_image, convert_time, get_exif, get_decimal_coordinates, download_result

def extract_image_metadata(db_manager):
    """Extract and display metadata from uploaded images"""
    st.header("Image Metadata Extraction")
    img_file = st.file_uploader("Upload Image...", type=['png', 'jpeg', 'jpg'])
    if img_file:
        display_image_metadata(img_file, db_manager)

def display_image_metadata(img_file, db_manager):
    """Display metadata for an uploaded image file"""
    with st.expander("Image File Stats"):
        stat_info = os.stat(img_file.readable())
        img_details = {
            "File Name": img_file.name,
            "Image Size": img_file.size,
            "Image Format": img_file.type,
            'Accessed Time': convert_time(stat_info.st_atime),
            'Creation Time': convert_time(stat_info.st_ctime),
            'Modified Time': convert_time(stat_info.st_mtime)
        }
        img_details_df = pd.DataFrame(list(img_details.items()), columns=['Meta Tags', 'Value'])
        st.dataframe(img_details_df, use_container_width=True)

    with st.expander('View Image'):
        img = load_image(img_file)
        st.image(img)

    with st.expander("Default(JPEG)"):
        img = load_image(img_file)
        img_details = {
            "Format": img.format,
            "Format Description": img.format_description,
            "File Size": img.size,
            "Height": img.height,
            "Width": img.width,
            "Info": img.info,
        }
        img_details_pillow_df = pd.DataFrame(list(img_details.items()), columns=['Meta Tags', 'Value'])
        st.dataframe(img_details_pillow_df, use_container_width=True)

    with st.expander("EXIF Data"):
        meta_tags = exifread.process_file(img_file)
        df_img_exifread = pd.DataFrame(list(meta_tags.items()), columns=["Meta Tags", "Value"])
        st.dataframe(df_img_exifread, use_container_width=True)

    with st.expander("Image Geo Coordinates"):
        img_details_with_exif = get_exif(img_file)
        img_coordinates = get_decimal_coordinates(img_details_with_exif)
        st.write(img_coordinates)

    with st.expander("Download Metadata Results"):
        final_df = pd.concat([img_details_df, img_details_pillow_df, df_img_exifread])
        download_result(final_df)
