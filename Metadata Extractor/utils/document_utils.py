import os
from datetime import datetime
import pandas as pd
import streamlit as st
from PyPDF2 import PdfReader
from utils.file_utils import convert_time, download_result

def extract_document_metadata(db_manager):
    """Extract and display metadata from uploaded document files"""
    st.header("Document Metadata Extractor")
    doc_file = st.file_uploader("Upload Document...", type=['docx', 'pdf'])

    if doc_file:
        with st.expander("File Stats"):
            file_details = {
                "FileName": doc_file.name,
                "FileSize": doc_file.size,
                "FileType": doc_file.type,
            }
            st.write(file_details)

            statinfo = os.stat(doc_file.readable())
            stats_details = {
                "Accessed_Time": convert_time(statinfo.st_atime),
                "Creation_Time": convert_time(statinfo.st_ctime),
                "Modified_Time": convert_time(statinfo.st_mtime),
            }
            file_details_combined = {**file_details, **stats_details}

            df_file_details = pd.DataFrame(list(file_details_combined.items()), columns=["Meta Tags", "Value"])
            st.dataframe(df_file_details, use_container_width=True)
            db_manager.add_file_details(doc_file.name, doc_file.type, doc_file.size, datetime.now())

        with st.expander("Metadata"):
            pdf_file = PdfReader(doc_file)
            pdf_info = pdf_file.metadata
            pdf_info_str = {k: str(v) for k, v in pdf_info.items()}
            df_file_details_with_pdf = pd.DataFrame(list(pdf_info_str.items()), columns=["Meta Tags", "Value"])
            st.dataframe(df_file_details_with_pdf, use_container_width=True)

        with st.expander("Download Results"):
            final_df = pd.concat([df_file_details, df_file_details_with_pdf])
            st.dataframe(final_df, use_container_width=True)
            download_result(final_df)
