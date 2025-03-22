import time
import tweepy
import os
from dotenv import load_dotenv

load_dotenv()

#variables globales
CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
BEARER_TOKEN = os.getenv("BEARER_TOKEN")

def create_client():
    return tweepy.Client(
        consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET,
        access_token=ACCESS_TOKEN, access_token_secret=ACCESS_TOKEN_SECRET
    )

def send_tweet(text):
    client = create_client()
    response = client.create_tweet(text=text)
    print(f"Tweet enviado: https://twitter.com/user/status/{response.data['id']}")

def like_last_mention():
    client = tweepy.Client(
        bearer_token=BEARER_TOKEN,
        consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET,
        access_token=ACCESS_TOKEN, access_token_secret=ACCESS_TOKEN_SECRET
    )
    
    user = client.get_me()
    user_id = user.data.id
    
    while True:
        try:
            mentions = client.get_users_mentions(user_id, max_results=5, user_auth=True)  # Obtener las últimas menciones
            
            if mentions.data:
                last_mention_id = mentions.data[0].id
                client.like(last_mention_id, user_auth=True)
                print(f"Like dado al tweet: https://twitter.com/user/status/{last_mention_id}")
            else:
                print("No hay menciones recientes.")
            break
        except tweepy.errors.TooManyRequests:
            print("Se alcanzó el límite de solicitudes. Esperando 15 segundos...")
            time.sleep(15)
        except Exception as e:
            print(f"Error inesperado: {e}")
            break


def retweet_from_user(username):
    client = tweepy.Client(
        bearer_token=BEARER_TOKEN,
        consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET,
        access_token=ACCESS_TOKEN, access_token_secret=ACCESS_TOKEN_SECRET
    )
    
    user = client.get_user(username=username, user_auth=True)
    user_id = user.data.id
    
    while True:
        try:
            tweets = client.get_users_tweets(user_id, max_results=5, user_auth=True)  # Obtener los últimos tweets
            
            if tweets.data:
                for tweet in tweets.data:
                    client.retweet(tweet.id, user_auth=True)
                    print(f"Retweet realizado: https://twitter.com/{username}/status/{tweet.id}")
            else:
                print(f"No hay nuevos tweets de @{username}.")
            break
        except tweepy.errors.TooManyRequests:
            print("Se alcanzó el límite de solicitudes. Esperando 15 segundos...")
            time.sleep(15)
        except Exception as e:
            print(f"Error inesperado: {e}")
            break

def retweet_from_users(usernames):
    client = tweepy.Client(
        bearer_token=BEARER_TOKEN,
        consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET,
        access_token=ACCESS_TOKEN, access_token_secret=ACCESS_TOKEN_SECRET
    )
    
    for username in usernames:
        try:
            user = client.get_user(username=username, user_auth=True)
            user_id = user.data.id
            
            tweets = client.get_users_tweets(user_id, max_results=5, user_auth=True)  # Obtener los últimos tweets
            
            if tweets.data:
                for tweet in tweets.data:
                    client.retweet(tweet.id, user_auth=True)
                    print(f"Retweet realizado: https://twitter.com/{username}/status/{tweet.id}")
            else:
                print(f"No hay nuevos tweets de @{username}.")
        except tweepy.errors.TooManyRequests:
            print("Se alcanzó el límite de solicitudes. Esperando 15 segundos...")
            time.sleep(15)
        except Exception as e:
            print(f"Error inesperado con @{username}: {e}")

# Ejemplo de uso
#tweet_text = input("Ingrese el texto del tweet: ")
#send_tweet(tweet_text)

#like_last_mention()

target_user = input("Ingrese el nombre de usuario para hacer retweet: ")
retweet_from_user(target_user)