import streamlit as sl
from functions import *
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = sl.tabs(["Sep", "Oct", "Nov","Dec","Jan","Feb","Mar","Apr","May"])

with tab1:
   sl.header("September Meeting Attendance")
   show_meeting_sheet("September")
   sl.write(sl.session_state)
with tab2:
   sl.header("October Meeting Attendance")
with tab3:
   sl.header("November Meeting Attendance")

with tab4:
   sl.header("December Meeting Attendance")
with tab5:
   sl.header("January Meeting Attendance")
with tab6:
   sl.header("February Meeting Attendance")

with tab7:
   sl.header("March Meeting Attendance")
with tab8:
   sl.header("April Meeting Attendance")
with tab9:
   sl.header("May Meeting Attendance")
