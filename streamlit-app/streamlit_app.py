import streamlit as st
import pandas as pd

st.write("Hello world") 

uploaded_file = st.file_uploader("Upload Files",type=['mp4'])
if uploaded_file is not None:
    file_details = {"FileName":uploaded_file.name,"FileType":uploaded_file.type,"FileSize":uploaded_file.size}
     st.write(file_details)