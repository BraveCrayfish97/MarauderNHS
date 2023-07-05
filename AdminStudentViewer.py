import streamlit as sl
from functions import *

data = scan_all_students()
show_all_students(data['Items'])