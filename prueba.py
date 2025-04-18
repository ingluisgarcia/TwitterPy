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
        bearer_token=BEARER_TOKEN,
        consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET,
        access_token=ACCESS_TOKEN, access_token_secret=ACCESS_TOKEN_SECRET
    )

def send_tweet(text):
    client = create_client()
    response = client.create_tweet(text=text)
    print(f"Tweet enviado: https://twitter.com/user/status/{response.data['id']}")

def like_last_mention():
    client = create_client()
    
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

def like_tweet_by_tweetId(tweet_id):
    client = create_client()

    try:
        client.like(tweet_id, user_auth=True)
        print(f"Like dado al tweet: https://twitter.com/user/status/{tweet_id}")
    except tweepy.errors.TooManyRequests:
        print("Se alcanzó el límite de solicitudes. Intenta más tarde.")
    except Exception as e:
        print(f"Error al dar like: {e}")


def like_user_tweets(username):
    client = create_client()
    
    try:
        # Obtener el ID del usuario por su username
        user = client.get_user(username=username)
        user_id = user.data.id

        # Obtener los últimos tweets del usuario
        tweets = client.get_users_tweets(user_id, max_results=5, user_auth=True)
        
        if tweets.data:
            for tweet in tweets.data:
                try:
                    client.like(tweet.id, user_auth=True)
                    print(f"Like dado al tweet: https://twitter.com/{username}/status/{tweet.id}")
                    time.sleep(1)  # Pequeña pausa para evitar límite
                except tweepy.errors.TooManyRequests:
                    print("Límite de solicitudes alcanzado. Esperando 15 minutos...")
                    time.sleep(900)
        else:
            print(f"No se encontraron tweets recientes de @{username}")
    
    except Exception as e:
        print(f"Error: {e}")

def retweet_from_user(username):
    client = create_client()
    
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
            print("Se alcanzó el límite de solicitudes para retweets. Esperando 15 minutos...")
            time.sleep(900)
        except Exception as e:
            print(f"Error inesperado: {e}")
            break

def retweet_tweet_by_tweetId(tweet_id):
    client = create_client()

    try:
        client.retweet(tweet_id, user_auth=True)
        print(f"Retweet realizado: https://twitter.com/user/status/{tweet_id}")
    except tweepy.errors.TooManyRequests:
        print("Se alcanzó el límite de solicitudes. Intenta más tarde.")
    except Exception as e:
        print(f"Error al hacer retweet: {e}")

def retweet_from_users(usernames):
    client = create_client()
    
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
            time.sleep(900)
        except Exception as e:
            print(f"Error inesperado con @{username}: {e}")

def retweet_mentions():
    client = create_client()

    try:
        auth_user = client.get_me(user_auth=True)
        user_id = auth_user.data.id

        while True:
            try:
                # Obtener los últimos tweets donde se menciona al usuario autenticado
                mentions = client.get_users_mentions(id=user_id, max_results=5, user_auth=True)

                if mentions.data:
                    for tweet in mentions.data:
                        client.retweet(tweet.id, user_auth=True)
                        print(f"Retweet realizado: https://twitter.com/i/web/status/{tweet.id}")
                else:
                    print("No hay nuevas menciones.")
                break

            except tweepy.errors.TooManyRequests:
                print("Límite de solicitudes alcanzado. Esperando 15 segundos...")
                time.sleep(900)
            except Exception as e:
                print(f"Error inesperado: {e}")
                break

    except Exception as e:
        print(f"No se pudo obtener el usuario autenticado: {e}")


def reply_to_tweet(tweet_id, reply_text):
    client = create_client()

    response = client.create_tweet(
        text=reply_text,
        in_reply_to_tweet_id=tweet_id
    )
    print(f"Respuesta enviada: https://twitter.com/user/status/{response.data['id']}")

def auto_reply_to_mention(reply_text):
    client = create_client()

    user = client.get_me()
    user_id = user.data.id

    try:
        mentions = client.get_users_mentions(user_id, max_results=5, user_auth=True)

        if mentions.data:
            last_mention = mentions.data[0]
            username = last_mention.author_id  # Usamos ID porque el username no se incluye por defecto

            # Para obtener el username, hacemos una petición adicional
            user_info = client.get_user(id=username, user_auth=True)
            username_str = user_info.data.username

            full_reply = f"@{username_str} {reply_text}"
            response = client.create_tweet(
                text=full_reply,
                in_reply_to_tweet_id=last_mention.id
            )
            print(f"Respuesta automática enviada: https://twitter.com/user/status/{response.data['id']}")
        else:
            print("No hay menciones para responder.")
    except tweepy.errors.TooManyRequests:
        print("Se alcanzó el límite de solicitudes. Esperando 15 segundos...")
        time.sleep(900)
    except Exception as e:
        print(f"Error inesperado en auto-reply: {e}")

def obtener_y_responder_ultimo_tweet(nombre_usuario, mensaje_respuesta):
    client = create_client()
    
    # 1. Obtener ID del usuario
    usuario = client.get_user(username=nombre_usuario)
    user_id = usuario.data.id

    # 2. Obtener los últimos tweets del usuario (el primero es el más reciente)
    tweets = client.get_users_tweets(id=user_id, max_results=5)

    if tweets.data:
        tweet_id = tweets.data[0].id
        print(f"Último tweet ID: {tweet_id}")
        # 3. Responder al tweet
        reply_to_tweet(tweet_id, mensaje_respuesta)
    else:
        print("El usuario no tiene tweets recientes.")

# Ejemplo de uso
#tweet_text = input("Ingrese el texto del tweet: ")
#send_tweet(tweet_text)

#like_last_mention()

#mensaje = input("Escribe el mensaje")
usuario = "cymaniatico"
#reply_to_tweet("1907314722757591428", "A la espera de la siguiente temporada!")
#obtener_y_responder_ultimo_tweet(usuario, "Mis condolencias")
#retweet_mentions()
#retweet_from_user(usuario)
#like_user_tweets(usuario)
#like_tweet_by_tweetId("1907314722757591428")
retweet_tweet_by_tweetId("1905029441991963001")

