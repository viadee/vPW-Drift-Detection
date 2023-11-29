# Import necessary modules

from elasticsearch import Elasticsearch
from datetime import datetime, timedelta
import time
from collections import deque
from river.drift import binary
from configMessage import sendMessage

def process_elasticsearch_data(index, es):
    global threshold
    # Establish a connection to Elasticsearch
    MAX_QUEUE_SIZE = 150  # Increase the maximum queue size to 150
    last_processed_instances = deque(maxlen=MAX_QUEUE_SIZE)
    counter = 0
    average = 0

    # Initialize the drift detection model
    driftDetector = binary.HDDM_W()

    # Dictionary to store the mapping of activityId to a number
    activity_id_to_number = {}
    next_activity_number = 0  # Next available number

    while True:
        # Calculate the time 2 minutes ago from the current time in epoch_millis
        two_minutes_ago = int((datetime.now() - timedelta(minutes=2)).timestamp()) * 1000

        # Construct an Elasticsearch query to retrieve the latest documents
        query = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "range": {
                                "timestamp": {
                                    "gte": two_minutes_ago,
                                    "lte": "now"
                                }
                            }
                        }
                    ],
                    "filter": [
                        {
                            "exists": {
                                "field": "activityId"  # Ensure "activityId" exists in the document
                            }
                        }
                    ]
                }
            },
            "sort": {"timestamp": {"order": "asc"}},
            "size": 10000
        }

        # Perform the Elasticsearch query
        result = es.search(index=index, body=query)  # Adjust the index name
        hits = result["hits"]["hits"]

        # Iterate through the retrieved documents
        for hit in hits:
            activity_id = hit["_source"].get("activityId")
            activityInstanceId = hit["_source"].get("activityInstanceId")

            # If the activityId doesn't have a number assigned yet, assign one
            if activity_id not in activity_id_to_number:
                activity_id_to_number[activity_id] = next_activity_number
                next_activity_number += 1

            activity_number = activity_id_to_number[activity_id]

            # Check if the activity instance has already been processed
            if activityInstanceId in last_processed_instances:
                continue  # Skip already processed activities
            else:
                last_processed_instances.append(activityInstanceId)
                counter += 1
                average += activity_number
                if counter <= 1000:
                    threshold = average / counter
                else:
                    # Classify the activity as 1 or 0 based on the threshold
                    binary_classification = True if activity_number > threshold else False
                    driftDetector.update(binary_classification)
                    # If concept drift is detected, send a message
                    if driftDetector.drift_detected:
                        sendMessage.send_message_to_slack(f"A concept drift was recognized in ActivityId! Details in this query: {query} Timestamp: {datetime.now()}")

        time.sleep(60)  # Wait for 60 seconds before the next query

