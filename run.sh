#!/bin/sh

if [ -z "$YEAR" ]; then
  echo "年度を指定してください"
  exit 1
fi

rm -rf video/
mkdir video
python3 main.py "$YEAR"
cat data/"$YEAR"/*.csv > data/"$YEAR".csv
