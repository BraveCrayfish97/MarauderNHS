import streamlit as sl
from functions import *


if "logged_in" in sl.session_state:
    if sl.session_state["email"] in sl.session_state["admins"]:
        data = scan_all_pending()
        show_student_pending_hours(data['Items'])#this will show all students's pending hours cuz we are giving data that has all students
    else:
        sl.write("You do not have permission to view this page.")
else:
    sl.write("Please Login First")
