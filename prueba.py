import time
import tweepy
import os
from dotenv import load_dotenv

load_dotenv()
#datos de perfil test
#client id: WGN3WllyMnMyb3pjWWlyMndGbmI6MTpjaQ
#bearer_token: AAAAAAAAAAAAAAAAAAAAADGvzAEAAAAA8A5QoUXTiD2bHySrd3S4%2FOPsTpU%3DzjcfEfZFWdcDnVE6cuoGFd5CAR1QX9QkBDGhWflUQaExkeB1r1
#consumer_key = "q5LxnNhvIHGdVStwpdNfQthaq"
#consumer_secret = "2bn23gwwOCO4EltzJnPIW4h4TJWu4vLEr61zkN8ShHG3PsqyQc"
#access_token = "1889778308813824000-by07iVvCZVDpoBzgkKTwDv4FWypw28"
#access_token_secret = "Lnx4NepuTWehr7PNz5FEbhPRAF12UKzSbhVgGJtGcNBl4"

#datos de perfil cy
#client id= "N1phcDlXNUdKcFFMbnJzQnk5MHY6MTpjaQ"
#client secret = "S0VkaYcyhy4rDWOicB5uZ7HGg6NnchVDq-UzyTrmAgy2vtliML"
#bearer_token: "AAAAAAAAAAAAAAAAAAAAAFu7zwEAAAAAxNa3IE8S%2BxRjqcxvdGWlROaew4I%3DiBKsx81JQUruASyE1v9ytYujhFXl5AX7BCGawbkTY986uRbXqz"
#consumer_key = "zcNMT9hEQawsovx7X1rZMzwc3"
#consumer_secret = "T1pCwU6YNN3YXr8kZ8jGxzOurmNbAM3K9glml6oMpHDTjWPqhg"
#access_token = "86398919-NzbEg13HFUxnxe6EbittoAjR1dNRu5azKP5zBxpJl"
#access_token_secret = "3596TpI0kjgSuYRVU2XMFTJvDxnIplNQpwk1wuOhgI7dU"

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

# Ejemplo de uso
tweet_text = input("Ingrese el texto del tweet: ")
send_tweet(tweet_text)
#like_last_mention()