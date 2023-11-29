import time

from loadDataFromElastic import elasticsearchDataFetcherVariables
import threading

# Define a function to fetch data from Elasticsearch index
def fetcher(index, es):
    # Create an Elasticsearch connection to a local instance
    variableNames = []  # List to store unique variable names

    while True:
        # Construct an Elasticsearch query to find documents with "doubleValue" field
        query = {
            "query": {
                "exists": {"field": "doubleValue"}
            },
            "size": 100  # Retrieve up to 100 documents at a time
        }

        # Execute the Elasticsearch search query
        result = es.search(index=index, body=query)
        hits = result["hits"]["hits"]

        for hit in hits:
            variableName = hit["_source"].get("variableName")

            # Check if variableName has already been processed
            if variableName in variableNames:
                continue  # Skip if already processed
            else:
                variableNames.append(variableName)  # Add variableName to the list

                # Create a new thread to process the variableName
                thread = threading.Thread(target=elasticsearchDataFetcherVariables.process_elasticsearch_data, args=(index, variableName, es))
                thread.start()  # Start the thread to process the data

        # Sleep for 60 seconds before the next iteration
        time.sleep(60)