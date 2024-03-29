import streamlit as sl
from functions import *




if "logged_in" in sl.session_state:
    if sl.session_state["email"] in sl.session_state["admins"]:
        sl.title("View Any Student's Hours Here")
        std_email = sl.text_input("Enter Student's Email")
        std_viewed = sl.button("Display Student's Hours")

        if "std_viewed" not in sl.session_state:
            sl.session_state["std_viewed"] = std_viewed

        if std_viewed | sl.session_state["std_viewed"]:
            if std_email != "":
                sl.session_state["std_viewed"]=True
                data = query_for_email(std_email)
                show_student_hours(data['Items'])
    else:
        sl.write("You do not have permission to view this page.")
else:
    sl.write("Please Login First")
