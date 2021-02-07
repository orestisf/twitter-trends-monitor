# twitter-trends-monitor
A dockerized python app which uses Tweepy's Streamlistener class to track a list of hashtags, extract relevant tweet information and publishes them to an Azure Event Hub instance.

## Usage
The application accepts the following environmental variables:

- CONSUMER_KEY: Twitter dev app API key.
- CONSUMER_SECRET: Twitter dev app API key secret.
- ACCESS_KEY: Twitter def app acess token.
- ACCESS_SECRET: Twitter def app acess token secret.
- EVENTHUB_ENDPOINT: The event hub primary endpoint. Note that you need a Shared Access Key with at least WRITE permissions on the event hub.
- EVENTHUB_NAME: The event hub instance name.
- APP_INSIGHTS_KEY: The Azure Application Insights resource instrumentation key.
- RUNTIME_MINS: Set to an integer to indicate how many minutes the application will run. After the specified time is elapsed, the application will stop.
- QUERY_INTERVAL_SEC: Set to an integer to indicate the frequency 
- LOCATIONS: Insert a comma separated list of the locations for which to fetch trending topics. Example value: "Athens, Paris".