from keras.models import Sequential
from keras.layers import Dense
import numpy
import netfuncs

numpy.random.seed(42)

import MySQLdb

try:
    conn = MySQLdb.connect(host="127.0.0.1",user="root",passwd="exlsv",db="sakila")
except MySQLdb.Error as err:
    print("Connection error: {}", format(err))
    conn.close()
X_train, Y_train = netfuncs.get_meat_set(18, conn)
#X_test, Y_test = netfuncs.get_set_meat(18, conn)
X_train = numpy.asfarray(X_train)
Y_train = numpy.asfarray(Y_train)
mean = X_train.mean(axis=0)
std = X_train.std(axis=0)
X_train -= mean
X_train /= std
#X_test -= mean
#X_test /= std

# Создаем последовательную модель
model = Sequential()
print(X_train.shape[1])
# Добавляем уровни сети
model.add(Dense(150, input_shape=(36,), activation="relu"))
model.add(Dense(1))

# Компилируем модель
model.compile(loss="mean_squared_error", optimizer="adam", metrics=['mae'])

print(model.summary())

# Обучаем сеть
model.fit(X_train, Y_train, batch_size=1, epochs=500, verbose=2)

netfuncs.net_to_file(model, "neuro.json")

# Оцениваем качество обучения сети на тестовых данных
#mse, mae = model.evaluate(X_test, Y_test, verbose=0)
#print(mae)
