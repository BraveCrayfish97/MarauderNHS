import streamlit as sl
import boto3
from textract_kv_parser import parse
from datetime import datetime
import re
from functions import *


"""sl.markdown("<h1 style= 'text-align:center;'> Login Page </h1>", unsafe_allow_html=True)
with sl.form("Login Form"):
    col1, col2 = sl.columns(2)
    with col1:
        email = sl.text_input("Email",value="")
        
        print("added email to session " + email)
    with col2:
        password = sl.text_input("Password",value="")
    
    if sl.form_submit_button("Submit"):
        login(email, password)
        sl.session_state["email"] = email #so i can use it in HourViewer file
        if sl.session_state["email"] != "":
            sl.session_state["logged_in"] = True"""

sl.title("File Upload")
sl.markdown("---")

access_key = "AKIAQXLOFPE7NQYAORED"
secret_key = "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"
region="us-east-1"

textract_client = boto3.client("textract", aws_access_key_id=access_key, aws_secret_access_key=secret_key, region_name=region)
image = sl.file_uploader(label="Upload Here", type=["png", "jpg"])

if (image is not None) and (sl.session_state["logged_in"]):#then display the image
    sl.image(image)
    
    print(type(image.read()))
    image.seek(0)
    file_name = upload_to_s3(image, sl.session_state["email"])
    image.seek(0)
    """Document={
            'S3Object': {
                'Bucket': "nhsindividualhours",
                'Name': file_name
            }
        },"""
    response = textract_client.analyze_document(
        
        Document={'Bytes': image.read()},
        FeatureTypes=['FORMS']
    )
    
    
    #print("My Parse ------")
    #for block in response["Blocks"]:
    #    if block['BlockType'] == 'LINE':
    #        print(block['Text'])
    #print("-----------------\n\n\n")

    values = parse(response)
    location = values[0][0]
    start = values[1][0]
    end = values[2][0]
    hours = values[3][0]
    mins = values[4][0]
    desc = values[5][0]
    month = values[6][0]
    day = values[7]
    
    #day sometimes doesnt get key pair so find by going thru LINES
    if day is None:
        for block in response["Blocks"]:
            if block['BlockType'] == 'LINE':
                if "(Date)" in block['Text']:
                    day = re.sub("[^0-9]","", block['Text'])
    else:
        day = values[7][0]
                        
    
    #supervisor name and number separation
    firstDigit = "None"
    
    for i, c in enumerate(values[8][0]):
        if c.isdigit():
            firstDigit = i
            break

    if firstDigit=="None":
        supervisor_name = values[8][0]
        supervisor_number = "None"

    else:
        supervisor_name = values[8][0][0:firstDigit]
        supervisor_number =values[8][0][firstDigit:]

    #review page
    
    sl.markdown("### Review Page")
    with sl.form("Form 2"):
        col1, col2 = sl.columns(2)
        with col1:
            location = sl.text_input("Place of Service",value=location)
            hours = sl.text_input("Hours",value=hours)
            hours = int(hours.replace(" ",""))
            start = sl.text_input("Start Time",value=start)
            month = sl.text_input("Month", value=month)
            supervisor_name = sl.text_input("Supervisor Name",value=supervisor_name)

        with col2:
            desc = sl.text_input("Description of Activity",value=desc)
            mins = sl.text_input("Minutes",value=mins)
            mins = int(mins.replace(" ", ""))
            end = sl.text_input("End Time",value=end)
            day = sl.text_input("Day", value=day)
            supervisor_number = sl.text_input("Supervisor Phone Number",value=supervisor_number)
            
        #maybe? sl.date_input("Enter Date of Volunteer Service", datetime.date(2023,10,5))
        
        if sl.form_submit_button("Submit"):
            review_submit(sl.session_state["email"], location, desc, hours, mins, start, end , month, day, supervisor_name, supervisor_number,file_name)
    
    


    ## CODE FOR SAVING NEW FILE TO HERE
    ## FUTURE- put IMG in S3 w {Name}_timestamp w it having only year month and day not time
    #timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    #file_path = f"uploaded_image_{timestamp}.png"
    #file = open(file_path, "wb")
    #file.write(image.read())
    #file.close()
    
