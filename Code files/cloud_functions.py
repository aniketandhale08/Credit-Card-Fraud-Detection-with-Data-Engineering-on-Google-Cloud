import base64
import json
import smtplib
from google.cloud import secretmanager
from json import loads

def hello_pubsub(event, context):
    # Secret Manager credentials loading
    secret_client = secretmanager.SecretManagerServiceClient()
    project_id = "secret_manager_project_id"
    secret_response = secret_client.access_secret_version(
        {"name": "projects/"+project_id+"/secrets/smtp_credentials/versions/latest"}
    )
    secret_response = secret_response.payload.data.decode("utf-8")
    my_credentials = loads(secret_response)

    # SMTP server credentials fetched
    smtp_email = my_credentials["serv_mail"]
    smtp_password = my_credentials["password"]

    # Pub/Sub topic data loading
    pubsub_message = base64.b64decode(event["data"]).decode("utf-8")
    message_json = json.loads(pubsub_message)

    customer_email_pairs = [
        {"senders_name": "Wanda Bieker", "email": "your_mail_1"},
        {"senders_name": "Scott Surgeon", "email": "your_mail_2"},
        {"senders_name": "Rusty Younce", "email": "your_mail_1"},
        {"senders_name": "Sabine Baker", "email": "your_mail_2"},
        {"senders_name": "Pauline Russell", "email": "your_mail_1"},
        {"senders_name": "Angela Thomas", "email": "your_mail_2"},
        {"senders_name": "Virginia Polk", "email": "your_mail_1"},
        {"senders_name": "Josef Petersen", "email": "your_mail_2"},
        {"senders_name": "George Buffalo", "email": "your_mail_1"},
        {"senders_name": "Lisa Harvey", "email": "your_mail_2"},
        {"senders_name": "Hazel Jenkins", "email": "your_mail_1"},
        {"senders_name": "James Johnson", "email": "your_mail_2"},
        {"senders_name": "Carlos Nordstrom", "email": "your_mail_1"}
    ]

    bank_email_pairs = [
        {"SendersBank": "Barclays", "email": "your_mail_2"},
        {"SendersBank": "HSBC", "email": "your_mail_1"},
        {"SendersBank": "Standard Chartered", "email": "your_mail_2"},
        {"SendersBank": "UBS", "email": "your_mail_1"},
        {"SendersBank": "Wells Fargo", "email": "your_mail_2"},
        {"SendersBank": "BNP Paribas", "email": "your_mail_1"},
        {"SendersBank": "Citigroup", "email": "your_mail_2"},
        {"SendersBank": "JPMorgan Chase", "email": "your_mail_1"},
        {"SendersBank": "Deutsche Bank", "email": "your_mail_2"},
        {"SendersBank": "Credit Suisse", "email": "your_mail_1"},
        {"SendersBank": "Royal Bank of Canada", "email": "your_mail_2"},
        {"SendersBank": "Santander Group", "email": "your_mail_1"},
        {"SendersBank": "Goldman Sachs", "email": "your_mail_2"},
        {"SendersBank": "Bank of America", "email": "your_mail_1"}
    ]

    senders_name = message_json["senders_name"]
    SendersBank = message_json["SendersBank"]
    customer_email = ""
    bank_email = ""

    # Find the corresponding email addresses for the customer and bank
    for pair in customer_email_pairs:
        if pair["senders_name"] == senders_name:
            customer_email = pair["email"]
            break

    for pair in bank_email_pairs:
        if pair["SendersBank"] == SendersBank:
            bank_email = pair["email"]
            break

    if not customer_email:
        customer_email = "your_mail_1"
    if not bank_email:
        bank_email = "your_mail_2"

    # Send the email notifications
    email_subject_customer = "Fraud Transaction Detected!!"
    email_body_customer = f'''
Dear {senders_name},

We have detected a fraudulent transaction in your account. Details are as follows:

Type: {message_json['type']}
Transaction id: {message_json['id']}
Amount: {message_json['amount']}
Old Original Balance: {message_json['oldbalanceOrig']}
New Original Balance: {message_json['newbalanceOrig']}
Old Distination Balance: {message_json['oldbalanceDest']}
New Distination Balance : {message_json['newbalanceDest']}
Country of Transaction: {message_json['Country']}
senders_name : {message_json['senders_name']}
Receiver's Bank: {message_json['ReceiversBank']}
SendersBank :{message_json['SendersBank']}
receiver_name : {message_json['receiver_name']}
Date of transaction : {message_json['TransactionDates']}

Please contact our customer support (1800 1800) immediately if you have any concerns.

Thank you,
Transaction Admin Team,
TransactionPe Ltd.
'''

    email_subject_bank = "Fraud Transaction Alert - Action Required!!"
    email_body_bank = f'''
Dear Bank Representative,

A fraudulent transaction has been detected from one of your customers. Details are as follows:

Type: {message_json['type']}
Transaction id: {message_json['id']}
Amount: {message_json['amount']}
Old Balance (Origin): {message_json['oldbalanceOrig']}
New Balance (Origin): {message_json['newbalanceOrig']}
Old Balance (Destination): {message_json['oldbalanceDest']}
New Balance (Destination): {message_json['newbalanceDest']}
Country of Transaction: {message_json['Country']}
senders_name : {message_json['senders_name']}
Receiver's Bank: {message_json['ReceiversBank']}
SendersBank :{message_json['SendersBank']}
receiver_name : {message_json['receiver_name']}
TransactionDates : {message_json['TransactionDates']}

Please investigate and help us take appropriate action.

Thank you,
Transaction Admin Team,
TransactionPe Ltd.
'''

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(smtp_email, smtp_password)
            email_message_customer = f"Subject: {email_subject_customer}\nFrom: your_mail_1\nTo: {customer_email}\n\n{email_body_customer}"
            email_message_bank = f"Subject: {email_subject_bank}\nFrom: your_mail_1\nTo: {bank_email}\n\n{email_body_bank}"
            server.sendmail(smtp_email, customer_email, email_message_customer)
            server.sendmail(smtp_email, bank_email, email_message_bank)
        print("Emails sent successfully.")
    except Exception as e:
        print("Error sending emails:", str(e))

    print(pubsub_message)