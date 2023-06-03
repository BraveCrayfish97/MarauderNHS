import streamlit as sl
import boto3
from boto3.dynamodb.conditions import Key, Attr
from functions import *
import pandas as pd
access_key = "AKIAQXLOFPE7NQYAORED"
secret_key = "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"
region="us-east-1"

dynamodb = boto3.resource("dynamodb", aws_access_key_id=access_key, aws_secret_access_key=secret_key, region_name=region)
table=dynamodb.Table("NHS_Individual_Hours")


sl.title("View Hours Here")
viewed = sl.button("Click to see data")
if "viewed" not in sl.session_state:
    sl.session_state["viewed"] = viewed
if "logged_in" in sl.session_state:
    if viewed | sl.session_state["viewed"]:
        sl.session_state["viewed"]=True
        email = sl.session_state.get("email", "")

        data = query_for_email(email)
        show_student_hours(data['Items'])
            
        total_hours = calc_total_hours(data)
        sl.markdown("<h1> You have *"+str(total_hours)+"* hours </h1>", unsafe_allow_html=True)
else:
    sl.write("Please Login First")

