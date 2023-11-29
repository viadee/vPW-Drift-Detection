# Import necessary modules
from elasticsearch import Elasticsearch
from datetime import datetime, timedelta
import time
from collections import deque
from river.drift import binary
from configMessage import sendMessage

def process_elasticsearch_data(index, es):
    # Establish a connection to Elasticsearch


    MAX_QUEUE_SIZE = 30  # Maximum number of stored values
    last_processed_instances = deque(maxlen=MAX_QUEUE_SIZE)

    global threshold
    counter = 0
    average = 0

    # Initialize a binary drift detection model
    driftDetector = binary.HDDM_A()

    while True:
        # Calculate the time 5 minutes ago from the current time in epoch_millis
        five_minutes_ago = int((datetime.now() - timedelta(minutes=5)).timestamp()) * 1000

        # Elasticsearch query to retrieve the latest documents with "eventType" equal to "COMPLETED"
        query = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "match": {
                                "eventType": "COMPLETED"
                            }
                        },
                        {
                            "range": {
                                "timestamp": {
                                    "gte": five_minutes_ago,
                                    "lte": "now"
                                }
                            }
                        }
                    ]
                }
            },
            "sort": {"timestamp": {"order": "asc"}},
            "size": 10000
        }

        # Perform the Elasticsearch search
        result = es.search(index=index, body=query)  # Modify the index name
        hits = result["hits"]["hits"]

        # Iterate through the retrieved documents
        for hit in hits:
            processInstance = hit["_source"].get("processInstanceId")

            # Check if the process instance has been processed before
            if processInstance in last_processed_instances:
                continue  # Skip processing if already processed
            else:
                last_processed_instances.append(processInstance)
                output = hit["_source"].get("durationInMillis")
                counter += 1
                average += output
                if counter <= 1000:
                    # Update the threshold during the initial 50 observations
                    threshold = average / counter
                else:
                    # Classify as 1 if the output is greater than the threshold, else 0
                    binary_classification = True if output > threshold else False
                    # Update the drift detection model with the classification
                    driftDetector.update(binary_classification)
                    if driftDetector.drift_detected:
                        # Send a message to Slack if concept drift is detected in lead times
                        sendMessage.send_message_to_slack(f"A concept drift was recognized in lead times! Details in this query: {query} Timestamp: {datetime.now()}")

        time.sleep(60)  # Wait for 60 seconds before the next query


