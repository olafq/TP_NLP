from funciones import *
#FECHA ACTUAL 
if __name__ == '__main__':
#saco la fechas
    actual =datetime.date.today()
    ayer = actual - datetime.timedelta(1)
    mañana = actual +datetime.timedelta(1)
    fecha_actual = actual.strftime('%Y-%m-%d')
    fecha_mañana = mañana.strftime('%Y-%m-%d')
    fecha_ayer = ayer.strftime('%Y-%m-%d')
    fecha_ayer_reddit = ayer.strftime('%d,%m,%Y')
    print(fecha_ayer_reddit)
#DECLARACIONES DE VARIABLES PARA TWITTER y la consulta que se va hacer 
    tweets = []
    query = "(Bitcoin OR · OR $BTC) min_faves:100 until:2022-11-07 since:2022-10-06"

#DECLARACIONES DE VARIABLES PARA REDDIT
    subreddit = 'Bitcoin'
    limit = 100
    timeframe = fecha_ayer_reddit #hour, day, week, month, year, all
    listing = 'best' # controversial, best, hot, new, random, rising, top con el hot traemos los mas

    twetter = get_twitter(query,tweets,limit) 
    dr = get_auth_reddit(subreddit,listing,limit,timeframe) 
    reddit = get_post_reddit(dr) 
    cripto_noticias = get_post_criptoNoticias(query)
    reddit['sentimiento'] = (reddit['title'].apply(get_polarity)+ reddit['selftext'].apply(get_polarity)) # esto es para 
    twetter['sentimiento'] = twetter['tweets'].apply(get_polarity)
    cripto_noticias['sentimiento'] = (cripto_noticias['subtitulo'].apply(get_polarity)+ cripto_noticias['title'].apply(get_polarity))
    reddit['analisis'] = reddit['sentimiento'].apply(analysis)
    twetter['analisis'] = twetter['sentimiento'].apply(analysis)
    cripto_noticias['analisis'] = cripto_noticias['sentimiento'].apply(analysis)

    
    print(reddit) # muestro tabla de rediit que hablaron de bitcoin y su valor sentimental
    print(twetter)# muestro tabla de twits que hablaron de bitcoin y su valor sentimental
    print(cripto_noticias)# muestro tabla de titulo y subtitulo que hablaron de bitcoin y su valor sentimental
    
    sentimiento_total_twetter = sumarColumna(twetter['sentimiento']) 
    sentimiento_total_criptoNoticias = sumarColumna(cripto_noticias['sentimiento'])
    sentimiento_total_reddit = sumarColumna(reddit['sentimiento'])
    sentimiento_total = sentimiento_total_criptoNoticias+sentimiento_total_twetter+sentimiento_total_reddit
    
    print(sentimiento_total_twetter)
    print(sentimiento_total_reddit)
    print(sentimiento_total_criptoNoticias)
    print(sentimiento_total)
    

    pronostico_BTC = calculo_de_sentimiento(sentimiento_total)
    #print(pronostico_BTC)
    #print(ayer)
    precio1 = precio_fecha_open(fecha_ayer,fecha_actual) #precio de cierre de un dia antes del precio a predecir
    precio2 = precio_fecha_open(fecha_actual,fecha_mañana)#precio a predecir
    
    conectarse_a_SQL(pronostico_BTC,fecha_ayer,precio1,fecha_actual,precio2)
    


    
