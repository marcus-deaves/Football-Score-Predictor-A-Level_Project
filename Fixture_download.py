import csv
from datetime import datetime
import requests
from Private_info import apikey

## import all the modules that i need

url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"  # My API URL
querystring = {"league": "39", "season": "2022"}  # My query to the API
headers = {"X-RapidAPI-Key": apikey,
           "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"}  # The data to input to the API so that it knows whos accessing it.

response = requests.request("GET", url, headers=headers, params=querystring)  # collecting the responce from the API

fixture_dictionary = response.json()
list_of_fixtures = [fixture_dictionary["response"]][0]

match_info = [["game_week", "date", "time", "home_team", "away_team", "venue", "score_home", "score_away", "winner", 0]]
for x in range(len(list_of_fixtures)):
    game_week = list_of_fixtures[x]["league"]["round"]
    game_week = game_week.split()[3]
    timestamp = list_of_fixtures[x]["fixture"]["timestamp"]
    date_time = str(datetime.fromtimestamp(timestamp))
    date, time = date_time.split()
    home_team = list_of_fixtures[x]["teams"]["home"]["name"]
    away_team = list_of_fixtures[x]["teams"]["away"]["name"]
    venue = list_of_fixtures[x]["fixture"]["venue"]["name"]
    score_home = list_of_fixtures[x]["goals"]["home"]
    score_away = list_of_fixtures[x]["goals"]["away"]

    if list_of_fixtures[x]["fixture"]["status"]["elapsed"] is not None:
        if list_of_fixtures[x]["teams"]["home"]["winner"]:
            winner = home_team
        elif list_of_fixtures[x]["teams"]["away"]["winner"]:
            winner = away_team
        elif list_of_fixtures[x]["teams"]["home"]["winner"] is None:
            winner = "Draw"
    else:
        winner = "not played"
        score_home = "no score"
        score_away = "no score"
    match_info.append([game_week, date, time, home_team, away_team, venue, score_home, score_away, winner, timestamp])

match_info = sorted(match_info, key=lambda l: l[9], reverse=False)
for i in range(len(match_info)):
    match_info[i].pop()

with open("master_table.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(match_info)


def write_to_file(filename, output):
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(output)


fixture_list = [["game_week", "date", "time", "home_team", "away_team", "venue", "score_home", "score_away", "winner"]]
result_list = [["game_week", "date", "time", "home_team", "away_team", "venue", "score_home", "score_away", "winner"]]

match_info.pop(0)

for x in match_info:
    if x[8] == "not played":
        result_list.append(x)
    else:
        fixture_list.append(x)


write_to_file("fixture_list.csv", fixture_list)
write_to_file("result_list.csv", result_list)
