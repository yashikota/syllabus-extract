import sys

import extractor
import extractor.utility


def main():
    if len(sys.argv) != 2:
        print("年度を指定してください")
        return

    extractor.Scraper().main(sys.argv[1])


if __name__ == "__main__":
    main()
