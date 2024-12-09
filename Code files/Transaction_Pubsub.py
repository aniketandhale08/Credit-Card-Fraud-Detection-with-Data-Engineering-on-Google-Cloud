import csv
import time
import json
from google.cloud import pubsub_v1

project_id = 'your_project_id'
topic_name = 'credit_transaction'
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id,topic_name)

filename = 'file_path'
time_delay = 10

with open(filename, 'r') as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        # Convert the row to JSON or any desired format
        data = {
            'type': row['type'],
            'id': row['id'],
            'amount': float(row['amount']),
            'oldbalanceOrig': float(row['oldbalanceOrig']),
            'newbalanceOrig': float(row['newbalanceOrig']),
            'oldbalanceDest': float(row['oldbalanceDest']),
            'newbalanceDest': float(row['newbalanceDest']),
            'Country': row['Country'],
            'senders_name':row['senders_name'],
            'ReceiversBank':row['ReceiversBank'],
            'SendersBank':row['SendersBank'],
            'receiver_name':row['receiver_name'],
            'TransactionDates':row['TransactionDates']
        }

        # Encode the data as JSON
        message_data = json.dumps(data).encode('utf-8')
                
        # Publish the data to the Pub/Sub topic
        future= publisher.publish(topic_path, data=message_data)
        print("Published record:", data)

        try:
            # Wait for the result and check if it was successful
            message_id = future.result()
            print(f"Published message with ID: {message_id}")
        except Exception as e:
            print(f"Failed to publish message: {e}")

        # Introduce time delay
        time.sleep(time_delay)
        
