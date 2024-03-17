import sys

import extractor
import extractor.utility


def main() -> None:
    if not extractor.utility.is_args_year():
        print("引数がありません。")
        return

    extractor.Scraper().main(sys.argv[1])


if __name__ == "__main__":
    main()
