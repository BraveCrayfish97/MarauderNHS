import streamlit as sl
from functions import *

data = scan_all_pending()
show_student_pending_hours(data['Items'])#this will show all students's pending hours cuz we are giving data that has all students

