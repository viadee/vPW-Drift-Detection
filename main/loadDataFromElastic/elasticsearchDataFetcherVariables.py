# Import necessary libraries

from datetime import datetime, timedelta
import time
from collections import deque
from river.drift import binary
from configMessage import sendMessage

# Define a function for processing data from Elasticsearch
def process_elasticsearch_data(index, variable_name, es):
    # Establish a connection to Elasticsearch

    # Define the maximum number of stored values in the deque
    MAX_QUEUE_SIZE = 30
    last_processed_instances = deque(maxlen=MAX_QUEUE_SIZE)

    global threshold
    counter = 0
    average = 0

    # Initialize a binary drift detector
    driftDetector = binary.HDDM_W()

    while True:
        # Calculate the time 5 minutes ago from the current time in epoch milliseconds
        five_minutes_ago = int((datetime.now() - timedelta(minutes=5)).timestamp()) * 1000

        # Elasticsearch query to retrieve the latest documents
        query = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "match": {
                                "variableName": variable_name
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
                    ],
                    "filter": [
                        {
                            "exists": {
                                "field": "doubleValue"  # Include "doubleValue" if it exists in the document
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

            output = hit["_source"].get("doubleValue")
            # Check if the process instance has been processed before
            if processInstance in last_processed_instances:
                continue  # Skip processing if already processed
            else:
                last_processed_instances.append(processInstance)

                # Update the counter and average
                counter += 1
                average += output
                if counter <= 1000:
                    threshold = average / counter
                else:
                    # Determine binary classification based on threshold
                    binary_classification = True if output > threshold else False
                    # Update the drift detector with the binary classification
                    driftDetector.update(binary_classification)
                    # if a concept drift was detected send a Slack message
                    if driftDetector.drift_detected:
                        sendMessage.send_message_to_slack(f"A concept drift was recognized in {variable_name}! Details in this query: {query} Timestamp: {datetime.now()}")

        # Wait for 60 seconds before the next query
        time.sleep(60)
