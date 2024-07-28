import streamlit as st
import pandas as pd
from datetime import datetime
from utils.image_utils import extract_image_metadata, display_image_metadata
from utils.audio_utils import extract_audio_metadata
from utils.document_utils import extract_document_metadata
from utils.file_utils import convert_time, download_result
from configs.about import HOME_ABOUT, ABOUT
from database.db_manager import DatabaseManager


# Initialize database manager
db_manager = DatabaseManager()

# Basic web application configuration
st.set_page_config(
    page_title="Metadata Extractor",
    page_icon="📝",
    initial_sidebar_state="expanded",
    layout='centered'
)

def main():
    """Main function to run the Streamlit app"""
    st.title("Metadata Extractor")

    # Side Bar Configuration
    menu = ['Home', 'Image', 'Audio', 'Document Files', 'About']
    choice = st.sidebar.selectbox("Menu", menu)

    # Home Page
    if choice == 'Home':
        st.header("Home")
        st.image("app_data/metadata.png")
        st.info(HOME_ABOUT)
        st.markdown("---")

        col1, col2, col3 = st.columns(3)
        with col1:
            with st.expander("Get Image Metadata"):
                st.info("Image Metadata")
                st.text("Upload JPEG, JPG, PNG Images")
        with col2:
            with st.expander("Get Audio Metadata"):
                st.info("Audio Metadata")
                st.text("Upload MP3, OGG")
        with col3:
            with st.expander("Get Document Metadata"):
                st.info("Document Metadata")
                st.text("Upload DOCX, PDF")

    # Image Metadata Extraction Page
    elif choice == 'Image':
        extract_image_metadata(db_manager)

    # Audio Metadata Extraction Page
    elif choice == 'Audio':
        extract_audio_metadata(db_manager)

    # Document Metadata Extraction Page
    elif choice == 'Document Files':
        extract_document_metadata(db_manager)

    # About Page
    elif choice == 'About':
        st.write(ABOUT)

    db_manager.close()

if __name__ == '__main__':
    main()
