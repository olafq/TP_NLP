from matplotlib import scale
from funciones import *
#FECHA ACTUAL 
actual =datetime.date.today()
#actual = actual -datetime.timedelta(1) 
ayer = actual - datetime.timedelta(1)
mañana = actual +datetime.timedelta(1)
fecha_acual = actual.strftime('%Y-%m-%d')
fecha_mañana = mañana.strftime('%Y-%m-%d')
fecha_ayer = ayer.strftime('%Y-%m-%d')
fecha_ayer_reddit = ayer.strftime('%d,%m,%Y')
#DECLARACIONES DE VARIABLES PARA TWITTER
tweets = []
query = "(Bitcoin OR · OR $BTC) min_faves:100 until:2022-11-1 since:2022-10-31"#devuelve los tweets del 28/10/22

#DECLARACIONES DE VARIABLES PARA REDDIT
subreddit = 'Bitcoin'
limit = 100
timeframe = fecha_ayer_reddit #hour, day, week, month, year, all
listing = 'best' # controversial, best, hot, new, random, rising, top con el hot traemos los mas

get_auth_tw() # para conectrase a la api de tw
twetter = get_twitter(query,tweets,limit)
dr = get_auth_reddit(subreddit,listing,limit,timeframe)
reddit = get_post_reddit(dr) #devuelve los titulos y selftext relacionados a dr
cripto_noticias = get_post_criptoNoticias(query)
reddit['sentimiento'] = (reddit['title'].apply(get_polarity)+ reddit['selftext'].apply(get_polarity))
twetter['sentimiento'] = twetter['tweets'].apply(get_polarity)
cripto_noticias['sentimiento'] = (cripto_noticias['subtitulo'].apply(get_polarity)+ cripto_noticias['title'].apply(get_polarity))
reddit['analisis'] = reddit['sentimiento'].apply(analysis)
twetter['analisis'] = twetter['sentimiento'].apply(analysis)
cripto_noticias['analisis'] = cripto_noticias['sentimiento'].apply(analysis)

'''
print(reddit) # muestro tabla de rediit que hablaron de bitcoin y su valor sentimental
print(twetter)# muestro tabla de twits que hablaron de bitcoin y su valor sentimental
print(cripto_noticias)# muestro tabla de titulo y subtitulo que hablaron de bitcoin y su valor sentimental
'''
sentimiento_total_twetter = sumarColumna(twetter['sentimiento'])
sentimiento_total_criptoNoticias = sumarColumna(cripto_noticias['sentimiento'])
sentimiento_total_reddit = sumarColumna(reddit['sentimiento'])
sentimiento_total = sentimiento_total_criptoNoticias+sentimiento_total_twetter+sentimiento_total_reddit
'''
print(sentimiento_total_twetter)
print(sentimiento_total_reddit)
print(sentimiento_total_criptoNoticias)
print(sentimiento_total)
'''

pronostico_BTC = calculo_de_sentimiento(sentimiento_total)
#print(pronostico_BTC)
#print(ayer)
precio = precio_fecha_open(fecha_ayer,fecha_acual)
conectarse_a_SQL(pronostico_BTC,fecha_ayer,fecha_acual,precio)
