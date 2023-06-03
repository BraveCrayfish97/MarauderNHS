import streamlit as sl
import boto3
import uuid
from datetime import datetime
from boto3.dynamodb.conditions import Key, Attr

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
    
    cols   = sl.columns([0.5,3,2,1,1,1,2])
    fields = ["#","email", "month", "day", "hours", "mins","Button"]

    # header
    for col, field in zip(cols, fields):
        col.write("**"+field+"**")
    # rows
    for idx, row in enumerate(response):
        #sl.write(row)
        cols = sl.columns([0.5,3,2,1,1,1,2])
        cols[0].write(idx)
        for i in range(1,len(fields)-1):
            
            cols[i].write(row[fields[i]])
        placeholder = cols[len(fields)-1]
        show_more   = placeholder.button("more", key=idx, type="primary")
        if show_more:
            # rename button
            placeholder.button("Close", key=str(idx)+"_")
            # show image
            display_s3_file(row["filename"])
            
            
