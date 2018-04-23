from keras.models import model_from_json
import exlsv_module
import holidays


def get_meat_set(n, conn):
    x = []
    y = []
    allweeks = 30 * 16 // 7
    for i in range(allweeks - n):
        x.append([])
        for j in range(i + 1, n + i + 1):
            x[i].append(exlsv_module.count_loss_weekly(conn, j))
            x[i].append(holidays.week_holiday(j))
        y.append(exlsv_module.count_loss_weekly(conn, allweeks - n + i))
    return x, y


def get_xy_sets(table, n1, n2):
    x = []
    j = 0
    for i in range(n1, n2):
        x.append([])
        x[j].append(table[i]['2011_tonnage_millions'])
        x[j].append(table[i]['2012_tonnage_millions'])
        x[j].append(table[i]['2013_tonnage_millions'])
        x[j].append(table[i]['2014_tonnage_millions'])
        x[j].append(table[i]['2015_tonnage_millions'])
        j += 1

    y = []
    for i in range(n1, n2):
        y.append(table[i]['2016_tonnage_millions'])
    return x, y


def net_to_file(model, name):
    # Генерируем описание модели в формате json
    model_json = model.to_json()
    # Записываем модель в файл
    json_file = open(name, "w")
    json_file.write(model_json)
    json_file.close()
    model.save_weights("net_model.h5")


def net_from_file(name):
    # Загружаем данные об архитектуре сети из файла json
    json_file = open(name, "r")
    loaded_model_json = json_file.read()
    json_file.close()
    # Создаем модель на основе загруженных данных
    loaded_model = model_from_json(loaded_model_json)
    # Загружаем веса в модель
    loaded_model.load_weights("net_model.h5")
    return loaded_model
