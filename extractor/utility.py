import csv
import json
import unicodedata


def url(year: str, numbering: str) -> str:
    return f"https://www.portal.oit.ac.jp/CAMJWEB/slbssbdr.do?value(risyunen)={year}&value(semekikn)=1&value(kougicd)={numbering}&value(crclumcd)=10201200"


def department(value: str) -> str:
    with open("data/department.json", "r") as f:
        return json.load(f)[value]


def normalize(enter: str) -> str:
    return unicodedata.normalize("NFKC", enter)


def values() -> list:
    with open("data/department.json", "r") as f:
        return list(json.load(f).keys())


def get_dow_period(enter: str) -> str:
    dow_list = list()
    period_list = list()

    splitted = enter.split("@")
    for i in range(len(splitted)):
        try:
            term, dow, period = splitted[i].split(" ")
        except ValueError:
            dow = "未掲載"
            period = "未掲載"
        dow_list.append(dow)
        period_list.append(period)

    return "@".join(dow_list), "@".join(period_list)


def dow(enter: str) -> str:
    dow_list, period_list = get_dow_period(enter)
    return dow_list


def period(enter: str) -> str:
    dow_list, period_list = get_dow_period(enter)
    return period_list


def output(year: str, enter: list) -> None:
    with open(f"data/{year}.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerows(enter)
