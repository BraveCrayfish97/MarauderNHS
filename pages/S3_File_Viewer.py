import streamlit as sl
from functions import *

filename = sl.text_input("Enter S3 filename")
if sl.button("Display File"):
    display_s3_file(filename)
