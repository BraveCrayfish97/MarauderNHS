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
if sl.button("Click to see data"):
    email = sl.session_state.get("email", "")
    if email=="":
        sl.write("Please Login First")
    else:
        data = query_for_email(email)
        sl.dataframe(data['Items'])
        #df = pd.DataFrame(response)
        #df.to_html()
        
        total_hours = calc_total_hours(data)
        
        sl.markdown("<h1> You have *"+str(total_hours)+"* hours </h1>", unsafe_allow_html=True)


sl.write(sl.session_state)