import streamlit as sl
import pandas as pd
from functions import *

data = query_for_email("shalom")
sl.write(data['Items'])
df = pd.DataFrame(data['Items'])
df = df.drop(columns="UUID")
#loop i from 0,len(data["filename"])
for i in range(0, len(df["filename"])):
    df["filename"][i] = f"https://s3.amazonaws.com/nhsindividualhours/{df['filename'][i]}"
# Apply the display_image function to the 'image' column
#df['filename'].apply(make_link)
#Then created a new column
#df['image'] = df["filename"].apply( lambda x: display_image(x))
for index, row in df.iterrows():
    image_url = row['filename']
    sl.image(image_url, use_column_width=True)
df.to_html()
print(df)
sl.dataframe(df)

