cd $(dirname "$0")
rm owid-covid-data.csv
wget https://covid.ourworldindata.org/data/owid-covid-data.csv
python3 parse.py
# git add .
# git commit -m "Update covid data"
# git push origin master
