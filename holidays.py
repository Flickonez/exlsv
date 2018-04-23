import datetime


def is_holiday(daymon):
    a = {'01.01', '07.01', '23.02', '08.03', '01.05', '09.05', '12.06', '04.11'}
    return daymon in a


def week_holiday(nweek):
    first = [2016, 1, 1]
    d = (nweek - 1) * 7 + first[1] * first[2] - 1

    aa = datetime.date(first[0], first[1], first[2])

    for i in range(d, d + 7):
        bb = datetime.timedelta(days=i)
        cc = aa + bb
        curr = [str(cc.day), str(cc.month), str(cc.year)]
        if int(curr[0]) < 10:
            curr[0] = "0" + curr[0]
        if int(curr[1]) < 10:
            curr[1] = "0" + curr[1]
        if is_holiday(curr[0] + "." + curr[1]):
            return 1.0
    return 0.0
