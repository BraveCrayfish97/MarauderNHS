import streamlit as sl
from functions import *
import requests

sl.set_page_config(layout="wide",menu_items={
        'About': "# MarauderNHS\n### Created by Rishi Chapati and Daniel Wang."
    })

sl.markdown("<h1 style= 'text-align:center;'> Login Page </h1>", unsafe_allow_html=True)
sl.write(get_login_str(), unsafe_allow_html=True)

print("hey")

"""if sl.button('Sign-in'):
    email, name = auth_user()
    sl.session_state["email"] = email
    sl.session_state["name"] = name
    sl.session_state["auth"] = True
    sl.session_state['logged_in']=True"""
try:
    email, name = auth_user()
    sl.session_state["email"] = email
    sl.session_state["name"] = name
    sl.session_state["auth"] = True
    sl.session_state['logged_in']=True    
except:
    print("no work")

if 'auth' in sl.session_state:
    if sl.session_state['auth']==True:
        if check_if_new_student(sl.session_state["email"]):
            grade = sl.selectbox("Are you a junior or a senior",("","junior","senior"))
            if grade != "":#they picked
                #add to NHS_Students
                dynamodb.Table("NHS_Students").put_item(
                    Item={
                        'email': sl.session_state['email'],
                        'name': sl.session_state['name'],
                        'grade': grade
                        }
                )
                sl.write("Thanks for signing up. \nWelcome to Marauder NHS")
        else:#not new
            sl.write("Thanks for signing in")
#try out container method
sl.write(sl.session_state)

#try try except around just displayuser()



