from matplotlib import scale
from requests import post
from sqlalchemy import null
from yfinance import Ticker
from funciones import *
import  datetime
import matplotlib.pyplot as plt
from sklearn.preprocessing import   MinMaxScaler
#FECHA ACTUAL 
fecha_actual =datetime.date.today()
ayer = fecha_actual - datetime.timedelta(1)
fecha_ayer_reddit = ayer.strftime('%d,%m,%Y')
print (fecha_ayer_reddit)
#DECLARACIONES DE VARIABLES PARA TWITTER
tweets = []
query = "(Bitcoin OR · OR $BTC) min_faves:100 until:2022-10-31 since:2022-10-30"#devuelve los tweets del 28/10/22

#DECLARACIONES DE VARIABLES PARA REDDIT
subreddit = 'Bitcoin'
limit = 100
timeframe = '30,10,2022' #hour, day, week, month, year, all
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
#hacer funcion que agregue estas tablas a fturo para mas etetico

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
'''
print(sentimiento_total)
#hacer un print funcion para que imprima los reddit twetts rtc con texto y valor positivo o negativo, a futuro para hacerlo mas estetico 
#conectarse_a_SQL(reddit)
# quedaria guardar los tados en sql y hacer un sum de todos los sentiminetos y en relacion a eso dsumar todo y hacer analisis si va subir
#MUCHO POCO NADA, MUY POCO MUCHISIMO

pronostico_BTC = calculo_de_sentimiento(sentimiento_total)
print(pronostico_BTC)


conectarse_a_SQL(pronostico_BTC,sentimiento_total)


'''
# cargar los datos de yahoo finance 
company = 'BTC-USD'
ticker = yf.Ticker(company)
hist = ticker.history(start= '2012-1-1', end ='2020-1-1')

#preparar los datps 
scaler = MinMaxScaler(feature_range=(0,1))
scaled_data = scaler.fit_transform(hist['Close'].values.reshape(-1,1))

prediction_days = 100

x_train = []
y_train = []

for x in range(prediction_days,len(scaled_data)):
  x_train.append(scaled_data[x-prediction_days:x,0])
  y_train.append(scaled_data[x,0])

x_train,y_train = np.array(x_train),np.array(y_train)
x_train = np.reshape(x_train,(x_train.shape[0],x_train.shape[1],1))

x_train.shape

#Construir el modelo
model = Sequential()

model.add(GRU(units=50,return_sequences = True, input_shape=(x_train.shape[1],1)))
model.add(Dropout(0.2))
model.add(GRU(units=50,return_sequences = True))
model.add(Dropout(0.2))
model.add(GRU(units=50))
model.add(Dropout(0.1))
model.add(Dense(units=1))

model.compile(optimizer='adam', loss='mean_squared_error')

model.fit(x_train,y_train,epochs=2,batch_size=32)

#Cargar los datos del test
hist_test = ticker.history(start = '2020-1-1', end='2022-8-21')
actual_prices = hist_test["Close"].values

total_dataset = pd.concat((hist['Close'],hist_test['Close']),axis=0)
model_inputs = total_dataset[len(total_dataset)-len(hist_test)-prediction_days:].values
model_inputs = scaler.transform(model_inputs.reshape(-1,1))

x_test = []

for x in range(prediction_days,len(model_inputs)):
  x_test.append(model_inputs[x-prediction_days:x,0])

x_test = np.array(x_test)
x_test = np.reshape(x_test,(x_test.shape[0],x_test.shape[1],1))
predicted_prices = model.predict(x_test)
predicted_prices = scaler.inverse_transform(predicted_prices)
fig, ax = plt.subplots()
ax.plot(actual_prices,color="black",label=f"{company} real prices")
ax.plot(predicted_prices,color="blue",label=f"{company} predicted prices")
ax.legend()
plt.show()
rentability = 1
for i in range(1,len(actual_prices)):
  if predicted_prices[i] > actual_prices[i-1]:
    rentability*= actual_prices[i]/actual_prices[i-1]

print((rentability-1)*100,"%")


'''
