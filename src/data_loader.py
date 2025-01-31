import streamlit as st
import pandas as pd
import chardet
from typing import Optional, Dict, Any

class DataLoader:
    """Handles file uploads, encoding detection, and data validation."""

    @staticmethod
    def detect_encoding(file_path: str) -> str:
        """Detect file encoding using chardet."""
        with open(file_path, 'rb') as f:
            result = chardet.detect(f.read())
        return result['encoding']

    @staticmethod
    def load_csv(file) -> Optional[pd.DataFrame]:
        """Load a CSV file with robust encoding detection."""
        try:
            # Save the uploaded file temporarily
            with open("temp.csv", "wb") as f:
                f.write(file.getbuffer())
            
            # Detect encoding
            encoding = DataLoader.detect_encoding("temp.csv")
            
            # Load the CSV file
            df = pd.read_csv("temp.csv", encoding=encoding)
            return df
        except Exception as e:
            st.error(f"Error loading file: {e}")
            return None

# Example usage
# if __name__ == "__main__":
#     uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
#     if uploaded_file:
#         df = DataLoader.load_csv(uploaded_file)
#         if df is not None:
#             st.write(df.head())