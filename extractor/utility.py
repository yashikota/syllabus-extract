import csv
import json
import os
import sys
import unicodedata


def url(year: str, numbering: str) -> str:
    return f"https://www.portal.oit.ac.jp/CAMJWEB/slbssbdr.do?value(risyunen)={year}&value(semekikn)=1&value(kougicd)={numbering}&value(crclumcd)=10201200"


def is_args_year() -> bool:
    return len(sys.argv) > 1


def is_args_resume() -> bool:
    return len(sys.argv) > 2


def department(value: str) -> str:
    with open("data/department.json", "r") as f:
        return json.load(f)[value]


def departments() -> list:
    with open("data/department.json", "r") as f:
        data = list(json.load(f).keys())
        return data[int(sys.argv[2]):] if is_args_resume() else data


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

def output(year: str, department: str, enter: list) -> None:
    os.makedirs(f"data/{year}", exist_ok=True)

    with open(f"data/{year}/{department}.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerows(enter)
