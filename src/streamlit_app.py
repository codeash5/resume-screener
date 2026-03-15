import streamlit as st
import pandas as pd
import subprocess
import os
import sys

st.title("AI Resume Screener")
st.write("Upload resumes and screen them against job descriptions.")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

script_path = os.path.join(BASE_DIR, "resume_screener.py")
excel_path = os.path.join(PROJECT_ROOT, "data", "resume_scores_per_jd.xlsx")

if st.button("Run Resume Screening"):
    st.write("Running resume screening...")

    result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)

    if result.returncode == 0:
        st.success("Screening Complete!")

        if os.path.exists(excel_path):
            df = pd.read_excel(excel_path)
            st.dataframe(df)

            with open(excel_path, "rb") as file:
                st.download_button(
                    label="Download Results",
                    data=file,
                    file_name="resume_scores_per_jd.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        else:
            st.error(f"Excel file not found at: {excel_path}")
    else:
        st.error("Error while running screening script")
        st.text(result.stderr)