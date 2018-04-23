import numpy
import exlsv_module
import netfuncs
import MySQLdb

def exlsv_work():
    try:
        conn = MySQLdb.connect(host="127.0.0.1",user="root",passwd="exlsv",db="sakila")
    except MySQLdb.Error as err:
        print("Connection error: {}", format(err))
        conn.close()
    numpy.random.seed(42)

    X_test, Y_test = netfuncs.get_meat_set(18, conn)

    x = X_test[len(Y_test) - 1]
    model = netfuncs.net_from_file("neuro.json")
    model.compile(loss="mean_squared_error", optimizer="adam", metrics=['mae'])


    x1 = numpy.asfarray(x)
    x1 = x1.reshape((1, 36))
    y = model.predict(x1)
    prognos = y[0][0]
    losses = exlsv_module.count_loss(conn)
    profits = exlsv_module.count_profit(conn)
    kg_meat, loss_meat = exlsv_module.count_loss_meat(conn)
    return int(prognos), int(losses), int(profits), int(kg_meat), int(loss_meat)