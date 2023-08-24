import streamlit as sl
from functions import *


if "logged_in" in sl.session_state:
    if sl.session_state["email"] in sl.session_state["admins"]:
        data = scan_all_students()
        show_all_students(data['Items'])
    else:
        sl.write("You do not have permission to view this page.")
else:
    sl.write("Please Login First")
