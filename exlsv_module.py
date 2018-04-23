import datetime
import MySQLdb


def switch_commas(st):
    st = st.replace(",", ".")
    return st

def count_storno_loss(conn, loss):
    query = "SELECT Summ_Average_Price FROM myaso2"
    try:
        cur = conn.cursor(MySQLdb.cursors.DictCursor)
        cur.execute(query)
        data = cur.fetchall()
    except MySQLdb.Error as err:
        print("Query error: {}".format(err))
        conn.close()
    res = 0.0
    for item in data:
        st = item['Summ_Average_Price']
        st = switch_commas(st)
        res += float(st)
    return loss - res


def count_loss(conn):
    query = "SELECT Summ_Average_Price FROM myaso2 WHERE " \
        " Code_Move_Material_Type != '102' AND" \
        " Code_Move_Material_Type != '162' AND" \
        " Code_Move_Material_Type != '602' AND" \
        " Code_Move_Material_Type != '959' AND" \
        " Code_Move_Material_Type != '960' AND" \
        " Code_Move_Material_Type != '961' AND" \
        " Code_Move_Material_Type != '962' AND" \
        " Code_Move_Material_Type != 'Z50' AND" \
        " Code_Move_Material_Type != 'Z51'"
    try:
        cur = conn.cursor(MySQLdb.cursors.DictCursor)
        cur.execute(query)
        data = cur.fetchall()
    except MySQLdb.Error as err:
        print("Query error: {}".format(err))
        conn.close()
    loss = 0.0
    for item in data:
        st = item['Summ_Average_Price']
        st = switch_commas(st)
        loss += float(st)
    return loss


def form_dict(year):
    if year % 4 == 0:
        res = {1 : 31,
               2 : 29,
               3 : 31,
               4 : 30,
               5 : 31,
               6 : 30,
               7 : 31,
               8 : 31,
               9 : 30,
               10 : 31,
               11 : 30,
               12 : 31}
    else:
        res = {1 : 31,
               2 : 28,
               3 : 31,
               4 : 30,
               5 : 31,
               6 : 30,
               7 : 31,
               8 : 31,
               9 : 30,
               10 : 31,
               11 : 30,
               12 : 31}
    return res


def count_loss_weekly(conn, nweek):
    first = [2016, 1, 1]
    d = (nweek - 1) * 7 + first[1] * first[2] - 1

    aa = datetime.date(int(first[0]), int(first[1]), int(first[2]))

    for i in range(d, d + 7):
        bb = datetime.timedelta(days=i)
        cc = aa + bb
        curr = [str(cc.day), str(cc.month), str(cc.year)]
        if int(curr[0]) < 10:
            curr[0] = "0" + curr[0]
        if int(curr[1]) < 10:
            curr[1] = "0" + curr[1]
        query = "SELECT Summ_Average_Price FROM myaso2 WHERE " \
            "Date = '" + curr[0] + "." + curr[1] + "." + curr[2] + "' AND" \
            " Code_Move_Material_Type != '102' AND" \
            " Code_Move_Material_Type != '162' AND" \
            " Code_Move_Material_Type != '602' AND" \
            " Code_Move_Material_Type != '959' AND" \
            " Code_Move_Material_Type != '960' AND" \
            " Code_Move_Material_Type != '961' AND" \
            " Code_Move_Material_Type != '962' AND" \
            " Code_Move_Material_Type != 'Z50' AND" \
            " Code_Move_Material_Type != 'Z51'"
        try:
            cur = conn.cursor(MySQLdb.cursors.DictCursor)
            cur.execute(query)
            data = cur.fetchall()
        except MySQLdb.Error as err:
            print("Query error: {}".format(err))
            conn.close()
        loss = 0.0

        for item in data:
            st = item['Summ_Average_Price']
            st = switch_commas(st)
            loss += float(st)
    return loss


def count_loss_meat(conn):
    codes = [102, 161, 532, 702, 950, 951, 952]
    # res1 - quantity res2 - sum of loss
    res1 = 0.0
    res2 = 0.0
    for c in codes:
        query = "SELECT Summ_Average_Price, Quantity FROM myaso2 WHERE Code_Move_Material_Type = " + str(c)
        try:
            cur = conn.cursor(MySQLdb.cursors.DictCursor)
            cur.execute(query)
            data = cur.fetchall()
        except MySQLdb.Error as err:
            print("Query error: {}".format(err))
            conn.close()

        for item in data:
            st1 = item['Quantity']
            st1 = switch_commas(st1)
            res1 += float(st1)
            st2 = item['Summ_Average_Price']
            st2 = switch_commas(st2)
            res2 += float(st2)
    return res1, res2


# Возможно, работает непраильно :-(
def count_profit(conn):
    query = "SELECT Summ_Check_Price FROM myaso2"
    try:
        cur = conn.cursor(MySQLdb.cursors.DictCursor)
        cur.execute(query)
        data = cur.fetchall()
    except MySQLdb.Error as err:
        print("Query error: {}".format(err))
        conn.close()
    profit = 0.0
    for item in data:
        st = item['Summ_Check_Price']
        st = switch_commas(st)
        profit += float(st)
    return profit - count_loss(conn)


# Динамика убыли. Делим наш доход(с убылью) на доход, который мы могли бы в идеале получить и получаем динамику убыли за этот период.
def dynamic_loss_manual(conn):
    query = "SELECT Summ_Check_Price FROM myaso2"
    try:
        cur = conn.cursor(MySQLdb.cursors.DictCursor)
        cur.execute(query)
        data = cur.fetchall()
    except MySQLdb.Error as err:
        print("Query error: {}".format(err))
        conn.close()
    profit = 0.0
    for item in data:
        st = item['Summ_Check_Price']
        st = switch_commas(st)
        profit += float(st)
    return ((profit - count_loss(conn)) / profit) * 100

