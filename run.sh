YEAR=2024

rm -rf video/
mkdir video
python3 main.py "$YEAR"
cat data/"$YEAR"/*.csv > data/"$YEAR".csv
