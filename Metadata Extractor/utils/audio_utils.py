import os
import pandas as pd
import streamlit as st
from datetime import datetime
from mutagen import File as MutagenFile
from utils.file_utils import convert_time, download_result

def extract_audio_metadata(db_manager):
    """Extract and display metadata from uploaded audio files"""
    st.header("Audio Metadata Extractor")
    audio_file = st.file_uploader("Upload Audio...", type=['mp3', 'ogg'])

    if audio_file:
        with st.expander("Play Audio"):
            st.audio(audio_file.read())

        with st.expander("File Stats"):
            file_details = {
                "FileName": audio_file.name,
                "FileSize": audio_file.size,
                "FileType": audio_file.type,
            }
            st.write(file_details)

            statinfo = os.stat(audio_file.readable())
            stats_details = {
                "Accessed_Time": convert_time(statinfo.st_atime),
                "Creation_Time": convert_time(statinfo.st_ctime),
                "Modified_Time": convert_time(statinfo.st_mtime),
            }
            st.write(stats_details)

            file_details_combined = {
                **file_details,
                **stats_details
            }

            df_file_details = pd.DataFrame(list(file_details_combined.items()), columns=["Meta Tags", "Value"])
            st.dataframe(df_file_details)

            db_manager.add_file_details(audio_file.name, audio_file.type, audio_file.size, datetime.now())

        with st.expander("Metadata with Mutagen"):
            audio_details = MutagenFile(audio_file)
            audio_details_str = {k: str(v) for k, v in audio_details.items()}
            df_audio_details_with_mutagen = pd.DataFrame(list(audio_details_str.items()), columns=["Meta Tags", "Value"])
            st.dataframe(df_audio_details_with_mutagen, use_container_width=True)

        with st.expander("Download Results"):
            final_df = pd.concat([df_file_details, df_audio_details_with_mutagen])
            st.dataframe(final_df)
            download_result(final_df)
