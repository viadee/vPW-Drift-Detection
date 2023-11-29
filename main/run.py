from elasticsearch import Elasticsearch
from loadDataFromElastic import elasticsearchDataFetcherActivityId, elasticsearchDataFetcherLeadTime
import multiVariablesFetcher
import threading
import os

def run(index):
    try:
        es = Elasticsearch('http://host.docker.internal:9200')
        activities = threading.Thread(target=elasticsearchDataFetcherActivityId.process_elasticsearch_data, args=(index, es))
        leadTime = threading.Thread(target=elasticsearchDataFetcherLeadTime.process_elasticsearch_data, args=(index, es))
        multi = threading.Thread(target=multiVariablesFetcher.fetcher, args=(index, es))

        activities.start()
        leadTime.start()
        multi.start()
        print("start")


    except Exception as e:
        print(f"Fehler beim Ausführen der Funktionen: {str(e)}")

index = os.getenv('INDEX')
run(index)
