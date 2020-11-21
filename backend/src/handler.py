import tweepy
import boto3
from botocore.exceptions import ClientError
import base64
import json
from collections import Counter
import time
import matplotlib.pyplot as plotter


supported_languages = ['ar', 'hi', 'ko', 'zh-TW', 'ja', 'zh', 'de', 'pt', 'en', 'it', 'fr', 'es']

comprehend = boto3.client(service_name='comprehend', region_name='us-east-1')

# DETECTS TEXT LANGUAGE WITH AMAZON COMPREHEND FROM TEXT
def get_dominant_language_code(t):
    language = comprehend.detect_dominant_language(Text = t)
    language_code = language["Languages"][0]["LanguageCode"]
    return language_code

def get_entities(language_code, t):

    entities = comprehend.detect_entities(Text=t, LanguageCode=language_code)
    people_mentions = []
    organizations_mentions = []
    for entity in entities["Entities"]:
        if entity["Type"] == "PERSON":
            people_mentions.append(entity["Text"])
        if entity["Type"] == "ORGANIZATION":
            organizations_mentions.append(entity["Text"])
    return (people_mentions, organizations_mentions)

def get_sentiment(language_code, t):
    try:
        sentiment = comprehend.detect_sentiment(Text=t, LanguageCode=language_code)
        return sentiment["Sentiment"]
    except:
        return "UNDEFINED"


def get_secret(secret):

    secret_name = "twitter_sentiment_analysis"
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    # In this sample we only handle the specific exceptions for the 'GetSecretValue' API.
    # See https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
    # We rethrow the exception by default.

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            # An error occurred on the server side.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            # You provided an invalid value for a parameter.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            # You provided a parameter value that is not valid for the current state of the resource.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            # We can't find the resource that you asked for.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
    else:
        # Decrypts secret using the associated KMS CMK.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if 'SecretString' in get_secret_value_response:
            s = json.loads(get_secret_value_response['SecretString'])[secret]
            return s
        else:
            decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])[secret]
            return decoded_binary_secret
            



def main(event, context):

    start_time = time.time()

    print(event)
    
    search_type = event["query"]["search_type"]
    search_key = event["query"]["search_key"]

    print(search_type)
    print(search_key)

    # AUTHENTICATE TO TWITTER
    print("Authenticating to Twitter")
    auth = tweepy.OAuthHandler(get_secret('api_key'), get_secret('api_secret_key'))
    auth.set_access_token(get_secret('access_token'), get_secret('access_token_secret'))

    # CREATE TWITTER API OBJECT
    api = tweepy.API(auth)

    words_list = []
    sentiment_list = []
    language_list = []
    entity_people_list = []
    entity_organization_list = []

    try:
        api.verify_credentials()
        print("Authentication OK")
    except:
        print("Error during authentication")


    tweets = []

    # MAXIMUM COUNT IS 200 TWEETS
    if search_type == '@':
        print('Search @')
        tweets = api.user_timeline(screen_name=search_key, 
                                count=100,
                                include_rts = False,
                                tweet_mode = 'extended')
    elif search_type == '#':
        print('Search #')
        key = '#' + search_key
        tweets = tweepy.Cursor(api.search, q=key, rpp=100, include_rts = False, tweet_mode = 'extended').items(100)
        print(tweets)
    else:
        print("Invalid Search Type: " + search_type)
        response = {
            "statusCode": 301,
            "body": {"error_message": "Busca inválida. Deve-se buscar por uma @ ou #."}
        }

        return response

    for tweet in tweets:
        language_code = get_dominant_language_code(tweet.full_text)
        language_list.append(language_code)

        words_list.extend(tweet.full_text.lower().split(" "))

        if language_code in supported_languages:
            entities = get_entities(language_code, tweet.full_text)
            entity_people_list.extend(entities[0])
            entity_organization_list.extend(entities[1])

            sentiment = get_sentiment(language_code, tweet.full_text)
            sentiment_list.append(sentiment)

    
    words_counter = {x: count for x, count in Counter(words_list).items() if (count >= 2 and 'http' not in x and len(x) >= 3)}
    language_counter = Counter(language_list)
    entity_people_counter = {x: count for x, count in Counter(entity_people_list).items() if count >= 2}
    entity_organization_counter = {x: count for x, count in Counter(entity_organization_list).items() if count >= 2}
    sentiment_counter = Counter(sentiment_list)

    print(language_counter)
    print(entity_people_counter)
    print(entity_organization_counter)
    print(sentiment_counter)

    print("--- %s seconds ---" % (time.time() - start_time))

    body = {
        "words": words_counter,
        "language": language_counter,
        "entity_people": entity_people_counter,
        "entity_organization": entity_organization_counter,
        "sentiment": sentiment_counter
    }

    response = {
        "statusCode": 200,
        "body": body
    }

    return response

