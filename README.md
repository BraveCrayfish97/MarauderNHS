# MarauderNHS
This web app serves as the offical website for Marcus High School's NHS. Along with displaying information about important dates for volunteering events and summaries about the latest meeting, it allows users to upload and manage their service hours and allows officers to verify them in an efficient manner.

## Features
- Upload NHS Hours: Users can upload their NHS hours by simply uploading a picture of their hour sheet, which is then scanned by AWS Textract.
- View Past Hours: Users can view and manage their past NHS service hours.
- Alerts/Hour Deadlines: The app provides alerts and notifications when deadlines for hour submission are approaching.

## Technologies Used

- Python
- Streamlit
- AWS
  - Textract - Image Reading
  - DynamoDB - Data Storage
  - S3 - Image Storage
  - EC2 - Website Hosting
