import csv
import time
import json
from google.cloud import pubsub_v1
project_id = 'final-year-project-438314'
topic_name = 'credit_transaction'
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id,topic_name)
filename = 'final-year-project/fraud_data.csv'
time_delay = 10
with open(filename, 'r') as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        # Convert the row to JSON or any desired format
        data = {
            'row_num': row['row_num'],
            'type': row['type'],
            'id': row['id'],
            'amount': row['amount'],
            'oldbalanceOrig': float(row['oldbalanceOrig']),
            'newbalanceOrig': float(row['newbalanceOrig']),
            'oldbalanceDest': float(row['oldbalanceDest']),
            'newbalanceDest': float(row['newbalanceDest']),
            'Country': row['Country'],
            'senders_name':row['senders_name'],
            'ReceiversBank':row['ReceiversBank'],
            'SendersBank':row['SendersBank'],
            'receiver_name':row['receiver_name'],
            'TransactionDates':row['TransactionDates'],
            'nameOrig':row['nameOrig'],
            'nameDest':row['nameDest']
        }

        message_data = json.dumps(data).encode('utf-8')
                
        # Publish the data to the Pub/Sub topic
        publisher.publish(topic_path, data=message_data)
        print("Published record:", data)

        # Introduce time delay
        time.sleep(time_delay)