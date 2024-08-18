import os

import extractor
import extractor.utility


def main():
    year: str = os.getenv("YEAR")
    if year == "":
        print("年度を指定してください")
        return

    extractor.Scraper().main(year)


if __name__ == "__main__":
    main()
