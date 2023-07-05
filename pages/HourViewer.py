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

if "logged_in" in sl.session_state:
    email = sl.session_state.get("email", "")

    data = query_for_email(email)
    show_student_hours(data['Items'])
            
    total_hours, approved_hours, denied_hours = calc_total_hours(data)
    sl.markdown(f"# Total Hours: {total_hours}")
    sl.markdown(f"### Approved Hours: {approved_hours}")
    sl.markdown(f"### Denied Hours: {denied_hours}")
    sl.markdown(f"### Pending Hours: {total_hours-approved_hours-denied_hours}")

else:
    sl.write("Please Login First")

