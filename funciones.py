from bs4 import BeautifulSoup
import json
import twint
from nltk.sentiment.vader import SentimentIntensityAnalyzer # vader muy bueno para analisiar textos cortos como los tweets  
import tweepy
import pandas as pd # clave para el prosesamiento de informacion de manera ordeanada 
import requests
import pyodbc
from sqlalchemy import case, create_engine, null, true
import snscrape.modules.twitter as sntwitter
import snscrape.modules.reddit as sntreddit
import nest_asyncio
nest_asyncio.apply()
#FUNCIONES PARA APIS 
#FUNCIONES PARA API TW
def get_auth_tw():#Para conectarse a la API de tw 
    API_KEY ="gSnawrypKwD2KJyV3m9uuvDp1"
    API_KEY_SECRET = "jUc2SGNOkCKJoqDdygEYMuQm3zhN3MHz2t2YCphkFlp44KWod9"
    ACCESS_TOKEN  = "1583200205222060058-vP4q8fUUMZjHW1IfpdukMa9karRcMf"
    ACCESS_TOKEN_SECRET  = "fqTJAhNWuKafOTo5l0iHTTn3w9eTSD7g9wPMxsFyLsWqS"
    auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    return auth


def get_twitter(query,tweets,limit):#Para obtener contenido del tweet sobre una palabra clave("query")
 for tweet in sntwitter.TwitterSearchScraper(query).get_items():
    if len(tweets) == limit:
        break
    else:
        if(tweet.user.followersCount>1000):
            tweets.append([ tweet.content, tweet.user.username])
 df =pd.DataFrame(tweets, columns=['tweets','username'])
 df.head()
 return df
# FUNCIONES API PARA REDDIT
def get_auth_reddit(subreddit,listing,limit,timeframe):
    try:
        base_url = f'https://www.reddit.com/r/{subreddit}/{listing}.json?limit={limit}&t={timeframe}'
        request = requests.get(base_url, headers = {'User-agent': 'yourbot'})
    except:
        print('An Error Occured')
    return request.json()

def get_post_reddit(r):
    '''
    Get a List of post titles
    '''
    df = pd.DataFrame()

    posts = []
    for post in r['data']['children']:
        if(post['data']['score']>100):
            df = df.append({
                'title': post['data']['title'],
                'author': post['data']['author'],
                'selftext': post['data']['selftext'],
            },ignore_index=true)
    return df

#FUNCIONES API PARA CRIPTO NOTICIAS 
def get_post_criptoNoticias(query):
    url = 'https://www.criptonoticias.com/?s=Bitcoin'
    pagina = requests.get(url)
    soup = BeautifulSoup(pagina.content,'html.parser')
    titulos = soup.find_all('h3',class_="jeg_post_title")  
    subtitulo = soup.find_all('div',class_="jeg_post_excerpt")

    posts =[]
    subtitutlos=[]
    for i in titulos:
        posts.append([i.text])
    df =pd.DataFrame(posts, columns=['title'])
    for i in subtitulo:
        subtitutlos.append([i.text])
    df['subtitulo'] = pd.DataFrame(subtitutlos, columns=['subtitle'])
    return df

#------------------------------------------------------------------------
#-------------------------------------------------------------------------
#GUARDAR DATOS EN LA SQL
#Guardar datos de un DataFrame en una bd SQL(MEJORAR ALGORITMO QUE NO FUNCIONA)
def pasar_a_lista(df):
    lista =df.values.tolist()
    return lista

def conectarse_a_SQL(lista):
    host =  "localhost",
    user = "sa",
    password = "12345",
    db = "NLP"
    try:
        connection = pyodbc.connect('DRIVER={SQL Server};SERVER=LAPTOP-4EK17G6N\SQLEXPRESS;DATABASE=NLP;UID=sa;PWD=12345')
        cursoInsert = connection.cursor()
        print("conexion exitosa")
        consulta = "INSERT INTO Posts_reddit(title,author,selftext,sentiment,analisis) VALUES(?,?,?,?,?);"
        '''
        No se porque tira fail al insertar la lista 
        for  x in lista:
            cursoInsert.execute(consulta,x)
        ''' 
        cursoInsert.commit()
        cursoInsert.close()
        print("conexion exitosa")
    except Exception as ex:
        print("fail")

 #------------------------------------------------------------------------
 #------------------------------------------------------------------------

 #ANALISIS DE SENTIMIENTOS 
def get_polarity(text):
    sid  = SentimentIntensityAnalyzer()
    sentimiento =  sid.polarity_scores(text)
    return sentimiento['compound']
    #return TextBlob(text).sentiment.polarity
def analysis(score):
    if score <0:
        return "negativo"
    elif score == 0:
        return "neutro"
    else:
        return "positivo"

#------------------------------------------------------------------------
#------------------------------------------------------------------------
# Funciones para simplificar codigo 
def sumarColumna(col):
    total_columna = col.sum()
    return total_columna
def calculo_de_sentimiento(sentimiento_total):
    if(sentimiento_total>=0 and sentimiento_total<=12):
        return "Se espera una bajada fuerte en e precio"
    elif(sentimiento_total>=13 and sentimiento_total<=17):
        return "Se espera una minima disminucion en el precio"
    elif(sentimiento_total>=18 and sentimiento_total<=19):
        return "se espera que no varie el precio"
    elif(sentimiento_total>=20 and sentimiento_total<=30):
        return "se espera un aumento en el precio"
    elif(sentimiento_total>=30 ):
        return "se espera un aumento fuerte en el precio"