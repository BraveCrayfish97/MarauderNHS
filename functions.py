import streamlit as sl
import boto3
import uuid
from datetime import datetime
from boto3.dynamodb.conditions import Key, Attr
import os
from numpy import void
import asyncio
# https://frankie567.github.io/httpx-oauth/oauth2/
from httpx_oauth.clients.google import GoogleOAuth2
from dotenv import load_dotenv
import requests

#GOOGLE OAUTH CONFIG-------------
load_dotenv('.env')

CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']
REDIRECT_URI = os.environ['REDIRECT_URI']
#---------------------------------

access_key = "AKIAQXLOFPE7NQYAORED"
secret_key = "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"
region="us-east-1"

dynamodb = boto3.resource("dynamodb", aws_access_key_id=access_key, aws_secret_access_key=secret_key, region_name=region)
s3 = boto3.client("s3", aws_access_key_id=access_key, aws_secret_access_key=secret_key, region_name=region)
   

def review_submit(email, location,desc, hours, mins, start, end, month, day, supervisor_name, supervisor_number,filename):
    print("submitting to db")
    id = str(uuid.uuid4())
    dynamodb.Table("NHS_Individual_Hours").put_item(
   Item={
        'email': email,
        'UUID':id,
        'location': location,
        'desc': desc,
        'hours': hours,
        'mins': mins,
        'start': start,
        'end': end,
        'month': month,
        'day': day,
        'supervisor_name': supervisor_name,
        'supervisor_number': supervisor_number,
        'filename': filename
    }
)
def login(email, password):
    print("nice you " + email + "logged in")

def upload_to_s3(image, email):
 
    timestamp = datetime.now().strftime("%m-%d-%Y_%H:%M:%S")
    file_name = timestamp +"__" + email+"__IndivdualHourSheet.png"
    #s3.upload_file(file_name, "nhsindividualhours", image)
    s3.put_object(Body=image, Bucket="nhsindividualhours",Key=file_name)
    return file_name
def display_s3_file(filename):
    response = s3.get_object(Bucket="nhsindividualhours",Key=filename)
    sl.image(response["Body"].read())
def query_for_email(email):
    response = dynamodb.Table("NHS_Individual_Hours").query(
        KeyConditionExpression=Key('email').eq(email)
    )
    return response

def calc_total_hours(response):
    total_hours = 0
    for item in response['Items']:
        total_hours+= item['hours']
    return total_hours

def display_image(url):
    sl.image(url, width=100)

def make_link(url):
    sl.markdown(f"[Hour Sheet]({url})")

def show_student_hours(response):
    
    cols   = sl.columns([0.5,3,2,1,1.5,1.5,2,2,2])
    fields = ["#","email", "month", "day", "hours", "mins", "location", "desc","Image"]

    # header
    for col, field in zip(cols, fields):
        col.write("**"+field+"**")
    # rows
    for idx, row in enumerate(response):
        #sl.write(row)
        cols = sl.columns([0.5,3,2,1,1.5,1.5,2,2,2])
        cols[0].write(idx)
        for i in range(1,len(fields)-1):
            
            cols[i].write(row[fields[i]])
        placeholder = cols[len(fields)-1]
        show_more   = placeholder.button("View Image", key=idx, type="primary")
        if show_more:
            # rename button
            placeholder.button("Close", key=str(idx)+"_")
            # show image
            display_s3_file(row["filename"])
def check_if_new_student(email):
    response = dynamodb.Table("NHS_Students").query(
        KeyConditionExpression=Key('email').eq(email)
    )
    return response['Items']==[]
#----------------------------
#GOOGLE OAUTH FUNCS
async def get_authorization_url(client: GoogleOAuth2, redirect_uri: str):
    authorization_url = await client.get_authorization_url(redirect_uri, scope=["profile", "email"])
    return authorization_url


async def get_access_token(client: GoogleOAuth2, redirect_uri: str, code: str):
    token = await client.get_access_token(code, redirect_uri)
    return token


async def get_email(client: GoogleOAuth2, token: str):
    user_id, user_email = await client.get_id_email(token)
    return user_id, user_email


def get_login_str():
    client: GoogleOAuth2 = GoogleOAuth2(CLIENT_ID, CLIENT_SECRET)
    authorization_url = asyncio.run(
        get_authorization_url(client, REDIRECT_URI))
    return f'''<a target = "_self" href ="{authorization_url}"> Sign In </a> '''


def auth_user() -> void:
    client: GoogleOAuth2 = GoogleOAuth2(CLIENT_ID, CLIENT_SECRET)
    # get the code from the url
    code = sl.experimental_get_query_params()['code']
    token = asyncio.run(get_access_token(
        client, REDIRECT_URI, code))
    #sl.write(token)
    user_id, user_email = asyncio.run(
        get_email(client, token['access_token']))
    sl.write(
        f"You're logged in as {user_email}")
    
    url = f'https://people.googleapis.com/v1/{user_id}'
    params = {
        'personFields': 'names'  # Specify the desired profile fields
    }
    headers = {
        'Authorization': f'Bearer {token["access_token"]}'
    }
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        profile_data = response.json()
        #sl.write(profile_data)
        name = profile_data['names'][0]['displayNameLastFirst']
        print(f'Name: {name}')
        return user_email, name
    else:
        print(f'Error retrieving user profile: {response.status_code}\nPlease try again.')
