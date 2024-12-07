#dataflow pipeline code to run 
import apache_beam as beam
import os
import argparse
import logging
import pandas as  pd
import datetime
from google.cloud import bigquery
import pytz
from oauth2client.client import GoogleCredentials
from datetime import datetime,date,timedelta
from apache_beam.options.pipeline_options import PipelineOptions, StandardOptions
from google.cloud import bigquery
from google.protobuf.json_format import MessageToJson


class readandwrite(beam.DoFn): 
      def process(self, context):
        #do prediction from vertex AI, and load to bigquery table
        import time
        import json
        from google.cloud import pubsub_v1
        import googleapiclient.discovery
        from google.cloud import bigquery
        from google.cloud import firestore
        from typing import Dict
        from google.cloud import aiplatform
        from google.protobuf import json_format
        from google.protobuf.struct_pb2 import Value
        from google.protobuf.json_format import MessageToJson
        project_id = "your_project_id"
        subscription_id = "credit_transaction_subscription"
        publish_topic="fraud-alert-topic"
        client_bigquery = bigquery.Client()
        publisher = pubsub_v1.PublisherClient()
        subscriber = pubsub_v1.SubscriberClient()
        subscription_path = subscriber.subscription_path(project_id, subscription_id)
        db = firestore.Client(project=project_id)
        max_messages = 1
        rows_to_insert = []
        while True:
            response = subscriber.pull(request={"subscription": subscription_path, "max_messages": max_messages})
            for received_message in response.received_messages:
                message = received_message.message
                data_dict = json.loads(message.data.decode('utf-8'))
                #store the record in firestore first
                timestamp = time.strftime("%Y%m%d%H%M%S")
                document_id = f"transaction_{timestamp}"
                # Create a new document reference in Firestore
                doc_ref = db.collection('transactions').document(document_id)
                # Set the data of the document with the transaction data
                doc_ref.set(data_dict)
                instance_dict = data_dict
                #print(data_dict)
                # The AI Platform services require regional API endpoints.
                # Initialize client that will be used to create and send requests.
                # This client only needs to be created once, and can be reused for multiple requests.
                client_options = {"api_endpoint": "us-central1-aiplatform.googleapis.com"}
                client = aiplatform.gapic.PredictionServiceClient(client_options=client_options)
                # Create the instance object
                instance = json_format.ParseDict(instance_dict, Value())
                instances = [instance]
                # Create the parameters object
                parameters_dict = {}
                parameters = json_format.ParseDict(parameters_dict, Value())
                # Endpoint details
                project = "ML_Model_project_ID"
                endpoint_id = "ML_Model_endpoint_id"
                location = "us-central1"
                endpoint = client.endpoint_path(project=project, location=location, endpoint=endpoint_id)
                # Perform the prediction
                response = client.predict(endpoint=endpoint, instances=instances, parameters=parameters)
                #print("response")
                prediction = response.predictions[0]
                # Extract the predicted_isFraud value
                predicted_isFraud = prediction["predicted_isFraud"]
                #print("predicted_isFraud:", predicted_isFraud)
                #print("Record:", data_dict)

                if predicted_isFraud == "1":
                    features_passed_to_check = json.loads(MessageToJson(instances[0]))
                    table_id = "bigquery_fraud_data_table"
                    topic_path = publisher.topic_path(project_id, publish_topic)
                    message_data = json.dumps(features_passed_to_check).encode('utf-8')
                    print(message_data)
                    publisher.publish(topic_path, message_data)
                    #print("Published record:", message_data)

                else:
                    features_passed_to_check = json.loads(MessageToJson(instances[0]))
                    table_id = "bigquery_non_fraud_data_table"
                    
                subscriber.acknowledge(request={"subscription": subscription_path, "ack_ids": [received_message.ack_id]})
                rows_to_insert.append(data_dict)
                load = client_bigquery.insert_rows_json(table_id, rows_to_insert)
                rows_to_insert = []  # Clear the list after inserting the rows

            
            time.sleep(10)
        
def run():    
       
    try: 
        parser = argparse.ArgumentParser()
    
        parser.add_argument(
            '--dfBucket',
            required=True,
            help= ('Bucket where JARS/JDK is present')
            )

        known_args, pipeline_args = parser.parse_known_args()
    
        global df_Bucket 
        df_Bucket = known_args.dfBucket
        pipeline_options = PipelineOptions(pipeline_args)
        pipeline_options.view_as(StandardOptions).streaming = True
        pcoll = beam.Pipeline(options=pipeline_options)
        logging.info("Pipeline Starts")
        dummy= pcoll | 'Initializing..' >> beam.Create(['1'])
        dummy_env = dummy | 'Processing' >>  beam.ParDo(readandwrite())
        p=pcoll.run()
        logging.info('Job Run Successfully!')
        p.wait_until_finish()
    except:
        logging.exception('Failed to launch datapipeline')
        raise    
if __name__ == '__main__':
    run()