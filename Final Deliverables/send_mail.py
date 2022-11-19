
import smtplib, ssl
## email.mime subclasses
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
## The pandas library is only for generating the current date, which is not necessary for sending emails
import pandas as pd

# Define the HTML document
def send_email(email):
    html = '''
        <h1 style='color:white; text-align:center;background-color:green;padding:8px 10px;border-radius:3px'>You are Eligible to Apply </h1>
        <img src='https://www.pngmart.com/files/1/Blushing-Emoji-PNG-File.png' style='margin-left:50%' width='150px' height = '150px'>
        <p style="text-align:center;">Thank you for visiting our website. Hope you had a great experience</p>
        '''

    # Set up the email addresses and password. Please replace below with your email address and password
    email_from = 'gcesuaep@gmail.com'
    password = 'terc awcj webf raiv'
    email_to = email

    # Generate today's date to be included in the email Subject
    date_str = pd.Timestamp.today().strftime('%Y-%m-%d')

    # Create a MIMEMultipart class, and set up the From, To, Subject fields
    email_message = MIMEMultipart()
    email_message['From'] = email_from
    email_message['To'] = email_to
    email_message['Subject'] = f'Prediction Report Email- {date_str}'
 
    # Attach the html doc defined earlier, as a MIMEText html content type to the MIME message
    email_message.attach(MIMEText(html, "html"))
    # Convert it as a string
    email_string = email_message.as_string()

    # Connect to the Gmail SMTP server and Send Email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(email_from, password)
        server.sendmail(email_from, email_to, email_string)

def fail_mail(email):
    html = '''
        <h1 style='color:white; text-align:center;background-color:green;padding:8px 10px;border-radius:3px'>You are not Eligible to Apply </h1>
        <img src='https://i.pinimg.com/564x/6b/91/e5/6b91e55e2ff7ca9133f7a25fba2d5b23.jpg' style='margin-left:50%' width='150px' height = '150px'>
        <p style="text-align:center;">Thank you for visiting our website. Hope you had a great experience</p>
        '''

    # Set up the email addresses and password. Please replace below with your email address and password
    email_from = 'gcesuaep@gmail.com'
    password = 'terc awcj webf raiv'
    email_to = email

    # Generate today's date to be included in the email Subject
    date_str = pd.Timestamp.today().strftime('%Y-%m-%d')

    # Create a MIMEMultipart class, and set up the From, To, Subject fields
    email_message = MIMEMultipart()
    email_message['From'] = email_from
    email_message['To'] = email_to
    email_message['Subject'] = f'Prediction Report Email- {date_str}'

    # Attach the html doc defined earlier, as a MIMEText html content type to the MIME message
    email_message.attach(MIMEText(html, "html"))
    # Convert it as a string
    email_string = email_message.as_string()

    # Connect to the Gmail SMTP server and Send Email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(email_from, password)
        server.sendmail(email_from, email_to, email_string)

def linear_mail(email,predict):
    html = f'''
    
        <img src='https://www.tenforce.com/wp-content/uploads/2020/08/undraw_approve_qwp7-e1603987686875.png' style='margin-left:50%' width='150px' height = '150px'>
        <h1 style='color:white; text-align:center;background-color:green;padding:8px 10px;border-radius:3px'>Your chance of eligibility is : </h1>
        <h3 style="text-align:center;font-size:24px;color:Green;padding:10px">{predict}</h3>
        <p style="text-align:center;">Thank you for visiting our website. Hope you had a great experience</p>
    
        '''

    # Set up the email addresses and password. Please replace below with your email address and password
    email_from = 'gcesuaep@gmail.com'
    password = 'terc awcj webf raiv'
    email_to = email

    # Generate today's date to be included in the email Subject
    date_str = pd.Timestamp.today().strftime('%Y-%m-%d')

    # Create a MIMEMultipart class, and set up the From, To, Subject fields
    email_message = MIMEMultipart()
    email_message['From'] = email_from
    email_message['To'] = email_to
    email_message['Subject'] = f'Prediction Report Email- {date_str}'
    # Attach the html doc defined earlier, as a MIMEText html content
    # type to the MIME message
    email_message.attach(MIMEText(html, "html"))
    # Convert it as a string
    email_string = email_message.as_string()

    # Connect to the Gmail SMTP server and Send Email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(email_from, password)
        server.sendmail(email_from, email_to, email_string)
