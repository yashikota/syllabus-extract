#!/bin/sh

if [ -z "$YEAR" ]; then
  echo "年度を指定してください"
  exit 1
fi

python3 main.py "$YEAR"
