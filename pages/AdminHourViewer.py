import streamlit as sl
from functions import *


sl.title("View Any Student's Hours Here")

std_email = sl.text_input("Enter Student's Email")
std_viewed = sl.button("Display Student's Hours")

if "std_viewed" not in sl.session_state:
    sl.session_state["std_viewed"] = std_viewed

if std_viewed | sl.session_state["std_viewed"]:
    sl.session_state["std_viewed"]=True
    data = query_for_email(std_email)
    show_student_hours(data['Items'])

