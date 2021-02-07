import tweepy
import os
import json
import sys
import geocoder
import time
import logging
from opencensus.ext.azure.log_exporter import AzureLogHandler
from azure.eventhub import EventHubProducerClient, EventData
from azure.eventhub.exceptions import EventHubError

consumer_key = os.environ['CONSUMER_KEY']
consumer_secret = os.environ['CONSUMER_SECRET']
access_key = os.environ['ACCESS_KEY']
access_secret = os.environ['ACCESS_SECRET']
connection_string = os.environ['EVENTHUB_ENDPOINT']
event_hub_name = os.environ['EVENTHUB_NAME']
application_insights_instrumentation_key = os.environ['APP_INSIGHTS_KEY']
runtime = int(os.environ['RUNTIME_MINS'])*60
queryIntervalSeconds = int(os.environ['QUERY_INTERVAL_SEC'])
locations = os.environ['LOCATIONS']

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

producer = EventHubProducerClient.from_connection_string(conn_str=connection_string,eventhub_name=event_hub_name)
def send_event_data_batch(producer, message):
    event_data_batch = producer.create_batch()
    event_data_batch.add(EventData(message))
    producer.send_batch(event_data_batch)

def getTrendingTopics(locations):
    for i in locations:
        try:
            g = geocoder.osm(i)
            print("Fetcing trending topics for location:", g)
            closest_loc = api.trends_closest(g.lat, g.lng)
            trendingTopics = api.trends_place(closest_loc[0]['woeid'])
            trendingTopicsJson = json.dumps(trendingTopics)
            with producer:
                send_event_data_batch(producer, trendingTopicsJson)
            print("Successfully processed trending topics for location:", g)
        except KeyError:
            continue
        except Exception:
            logger.warning("Unable to find location %s", g)
            continue

def convertLocations(string): 
    li = list(string.split(",")) 
    return li

if __name__ == "__main__":
    start_time = time.time()
    logger = logging.getLogger(__name__)
    logger.addHandler(AzureLogHandler(connection_string='InstrumentationKey='+application_insights_instrumentation_key))
    locations = convertLocations(locations) 
    print("Starting tracking trending topics for",runtime,"seconds at UTC time",time.strftime("%H:%M:%S",time.localtime()),"and for",len(locations),"locations:",locations)
    while True:
        if (time.time() - start_time) < runtime:
            trendingTopics = getTrendingTopics(locations)
            time.sleep(queryIntervalSeconds - ((time.time() - start_time) % queryIntervalSeconds))
        else:
            t = time.localtime()
            current_time = time.strftime("%H:%M:%S", t)
            print('Runtime limit of', runtime, ' seconds reached, stopping connection at UTC time.',current_time)
            sys.exit()