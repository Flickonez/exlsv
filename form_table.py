import exlsv_module
import dayofweek

def get_meat_set(n, conn):
    x = []
    y = []
    allweeks = 30 * 9 // 7
    for i in range(allweeks - n):
        x.append([])
        for j in range(i + 1, n + i + 1):
            x[i].append(exlsv_module.count_loss_weekly(conn, j))
            x[i].append(dayofweek.week_holiday(j))
        y.append(exlsv_module.count_loss_weekly(conn, allweeks - n + i))
    return x, y
