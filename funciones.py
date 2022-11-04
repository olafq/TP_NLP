from bs4 import BeautifulSoup # Uso esta libreria para 
from nltk.sentiment.vader import SentimentIntensityAnalyzer # vader muy bueno para analisiar textos cortos como los tweets  
import tweepy #Uso esta libreria para poder conectarme a la API de TW
import pandas as pd # clave para el prosesamiento de informacion de manera ordeanada 
import requests
import pyodbc
import matplotlib
from sqlalchemy import  true
import snscrape.modules.twitter as sntwitter# es para la API de twitter para poder obtener los twits
import datetime 
import yfinance as yf # es para la API de yahoo finance y podes sacar el precio de la cripto


#########################################################################              
######################FUNCIONES PARA APIS################################
#########################################################################

#########################
##FUNCIONES PARA API TW##
#########################

def get_auth_tw():#Para conectarse a la API de tw 
    API_KEY ="gSnawrypKwD2KJyV3m9uuvDp1"
    API_KEY_SECRET = "jUc2SGNOkCKJoqDdygEYMuQm3zhN3MHz2t2YCphkFlp44KWod9"
    ACCESS_TOKEN  = "1583200205222060058-vP4q8fUUMZjHW1IfpdukMa9karRcMf"
    ACCESS_TOKEN_SECRET  = "fqTJAhNWuKafOTo5l0iHTTn3w9eTSD7g9wPMxsFyLsWqS"
    auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    return auth


#Para obtener contenido del tweet sobre una palabra clave("query"), recorre los tweets hasta el limite, y guarda los tweets con mas de 1000 seguidores 
# esto se hizo asi para tener una mejor prediccion del precio tomando tweets de gente mas importantes. Guarda el contenido y usuario en el dataFrame df.
def get_twitter(query,tweets,limit):
    for tweet in sntwitter.TwitterSearchScraper(query).get_items():
        if len(tweets) == limit:
            break
        else:
            if(tweet.user.followersCount>1000):
                tweets.append([ tweet.content, tweet.user.username])
    df =pd.DataFrame(tweets, columns=['tweets','username'])
    df.head()
    return df



#############################
##FUNCIONES API PARA REDDIT##
#############################

#Para conectarse a la API de Reddit pasandole el subreddit(bitcoin), listing(para saber cuales traer,top,best,etc.),
#el limit para saber hasta cuanto traer y el timepo de los tweet que quiero trear.
def get_auth_reddit(subreddit,listing,limit,timeframe):
    try:
        base_url = f'https://www.reddit.com/r/{subreddit}/{listing}.json?limit={limit}&t={timeframe}'
        request = requests.get(base_url, headers = {'User-agent': 'yourbot'})
    except:
        print('An Error Occured')
    return request.json()

#Esta funcion crea un dataFrame df, y una lista Posts en el cual se guardan los posts con score mayor a 100, esto lo tomo asi para 
# poder hacer un analisis mejor tomando los reddit de mayor importancia. y inserto en el dataframe el titulo, author y el texto en si del post 
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


######################################
##FUNCIONES API PARA CRIPTO NOTICIAS##
###################################### 


def get_post_criptoNoticias(query):
    url = 'https://www.criptonoticias.com/?s=Bitcoin'
    pagina = requests.get(url)
    soup = BeautifulSoup(pagina.content,'html.parser') # trae el contenido de la pagina criptoNoticia
    titulos = soup.find_all('h3',class_="jeg_post_title") # trae los titulos de las noticias   
    subtitulo = soup.find_all('div',class_="jeg_post_excerpt") # trae el contenido del post que tiene relacionado al titulo de arriba 
    posts =[]  
    subtitutlos=[]
    for i in titulos: # con este for recorremos todas las noticias y guardamos cada titulo y subtitulo en el dataframe pd, a df. 
        posts.append([i.text])
    df =pd.DataFrame(posts, columns=['title'])
    for i in subtitulo:
        subtitutlos.append([i.text])
    df['subtitulo'] = pd.DataFrame(subtitutlos, columns=['subtitle'])
    return df


#########################################################################  
#####################GUARDAR DATOS EN LA SQL#############################
#########################################################################  


#Guardar datos de un DataFrame en una bd SQL(MEJORAR ALGORITMO QUE NO FUNCIONA)
def conectarse_a_SQL(pronostico_BTC,fecha_pronostico,fecha_a_predecir,precio_open,):

    try:
        connection = pyodbc.connect('DRIVER={SQL Server};SERVER=LAPTOP-4EK17G6N\SQLEXPRESS;DATABASE=NLP;UID=sa;PWD=12345')# me conecto a la base de dato SQL 
        cursoInsert = connection.cursor() # creo un cursor que se relaciona con connection de nuestra base ce datos
        consulta = "INSERT INTO sentimiento_relacionado(fecha_del_analisis, analisis,fecha_a_predecir,precio_open) VALUES(?,?,?,?);"# creo la consulta que queremos hacer
        cursoInsert.execute(consulta,fecha_pronostico,pronostico_BTC,fecha_a_predecir,precio_open) # ejecuto la consulta pasandole los datos que quiero que inserte en sus respectivas columnas
        cursoInsert.commit() #comiteo para que se guarde 
        cursoInsert.close() #cierro la conexion 
        print("conexion exitosa")
    except Exception as ex:
        print("fail")


########################################################################## 
#####################ANALISIS DE SENTIMIENTOS############################# 
##########################################################################

#analiso el sentimiento de cada posts con el sid.polarity_scores
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

# calculo el sentimineto en funcion del sentimineto total que es la suma de lso 3 sentiminetos 
def calculo_de_sentimiento(sentimiento_total):
    if(sentimiento_total>=0 and sentimiento_total<=7):
        return "Se espera una bajada fuerte en e precio"
    elif(sentimiento_total>=8 and sentimiento_total<16):
        return "Se espera una minima disminucion en el precio"
    elif(sentimiento_total>=16 and sentimiento_total<=30):
        return "se espera un aumento minimo en el precio"
    elif(sentimiento_total>=30 ):
        return "se espera un aumento fuerte en el precio"

######################################################################### 
##############Funciones para simplificar codigo##########################
######################################################################### 


def sumarColumna(col):
    total_columna = col.sum()
    return total_columna


def pasar_a_lista(df):
    lista =df.values.tolist()
    return lista

# con esto se obtiene el precio de apertura 
def precio_fecha_open(fecha_ayer,fecha_actual):
    btc = yf.Ticker("BTC-USD")
    data = btc.history(start=fecha_ayer, end=fecha_actual)
    a = pasar_a_lista(data)
    for x in a:
        a = None
        for c in x:
            if(a is None):
                a=2
                return c