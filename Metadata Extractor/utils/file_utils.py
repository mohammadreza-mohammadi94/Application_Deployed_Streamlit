import os
from datetime import datetime
import base64
import streamlit as st
import pandas as pd
from PIL import Image, ExifTags

def load_image(image_file):
    """Load an image file into a PIL Image object"""
    return Image.open(image_file)

def convert_time(mytime):
    """Convert a timestamp to a human-readable format"""
    return datetime.fromtimestamp(mytime).strftime('%Y-%m-%d %H:%M')

def get_exif(filename):
    """Extract EXIF data from an image file"""
    exif = Image.open(filename)._getexif()
    exif_data = {}

    if exif is not None:
        for key, value in list(exif.items()):
            name = ExifTags.TAGS.get(key, key)
            exif_data[name] = value
            if name == 'GPSInfo':
                gps_info = {}
                for gps_key in value.keys():
                    gps_name = ExifTags.GPSTAGS.get(gps_key, gps_key)
                    gps_info[gps_name] = value[gps_key]
                exif_data['GPSInfo'] = gps_info

    return exif_data

def get_decimal_coordinates(info):
    """Get the decimal coordinates from EXIF data"""
    for key in ['Latitude', 'Longitude']:
        if 'GPS'+key in info and 'GPS'+key+'Ref' in info:
            e = info['GPS'+key]
            ref = info['GPS'+key+'Ref']
            info[key] = (
                e[0][0]/e[0][1] +
                e[1][0]/e[1][1] / 60 +
                e[2][0]/e[2][1] / 3600
            ) * (-1 if ref in ['S', 'W'] else 1)

    if 'Latitude' in info and 'Longitude' in info:
        return [info['Latitude'], info['Longitude']]

def download_result(data):
    """Allow the user to download the extracted metadata as a CSV file"""
    csv_file = data.to_csv(index=False)
    b64 = base64.b64encode(csv_file.encode()).decode()
    st.markdown("### Download CSV File")
    timestr = datetime.now().strftime("%Y%m%d-%H%M%S")
    new_filename = f"metadata_result_{timestr}.csv"
    href = f'<a href="data:file/csv;base64,{b64}" download="{new_filename}">Click Here!</a>'
    st.markdown(href, unsafe_allow_html=True)
