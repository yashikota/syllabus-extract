import csv
import json
import os
import unicodedata


def url(year: str, numbering: str) -> str:
    return f"https://www.portal.oit.ac.jp/CAMJWEB/slbssbdr.do?value(risyunen)={year}&value(semekikn)=1&value(kougicd)={numbering}&value(crclumcd)=10201200"


def department(value: str) -> str:
    with open("data/department.json", "r") as f:
        return json.load(f)[value]


def departments() -> list:
    with open("data/department.json", "r") as f:
        return list(json.load(f).keys())


def index(department: str) -> int:
    with open("data/department.json", "r") as f:
        return list(json.load(f).keys()).index(department)


def normalize(enter: str) -> str:
    return unicodedata.normalize("NFKC", enter)


def dow_period(enter: str) -> str:
    splitted = enter.split("@")

    try:
        dow = [splitted[i].split(" ")[1] for i in range(len(splitted))]
        period = [splitted[i].split(" ")[2] for i in range(len(splitted))]
    except IndexError:
        dow = ["未掲載"]
        period = ["未掲載"]
    finally:
        return " ".join(dow), " ".join(period)


def output(year: str, enter: list) -> None:
    with open(f"data/{year}.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerows(enter)
