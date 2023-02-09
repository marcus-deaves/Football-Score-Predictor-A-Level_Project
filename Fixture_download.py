import csv
from datetime import datetime
import requests
from Private_info import apikey

url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
querystring = {"league": "39", "season": "2022"}
headers = {"X-RapidAPI-Key": apikey,
           "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"}

response = requests.request("GET", url, headers=headers, params=querystring)

fixture_dictionary = response.json()
list_of_fixtures = [fixture_dictionary["response"]]

match_info = [["game_week", "date", "time", "home_team", "away_team", "venue", "score_home", "score_away", "winner", 0]]
for x in range(len(list_of_fixtures[0])):
    game_week = list_of_fixtures[0][x]["league"]["round"]
    game_week = game_week.split()[3]
    timestamp = list_of_fixtures[0][x]["fixture"]["timestamp"]
    date_time = str(datetime.fromtimestamp(timestamp))
    date, time = date_time.split()
    home_team = list_of_fixtures[0][x]["teams"]["home"]["name"]
    away_team = list_of_fixtures[0][x]["teams"]["away"]["name"]
    venue = list_of_fixtures[0][x]["fixture"]["venue"]["name"]
    score_home = list_of_fixtures[0][x]["goals"]["home"]
    score_away = list_of_fixtures[0][x]["goals"]["away"]
    if score_home is not None:
        if score_home > score_away:
            winner = home_team
        elif score_away > score_home:
            winner = away_team
        elif score_away == score_home:
            winner = "draw"
    else:
        winner = "not played"
        score_home = "no score"
        score_away = "no score"
    match_info.append([game_week, date, time, home_team, away_team, venue, score_home, score_away, winner, timestamp])
    print(type(timestamp))

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


file = open("master_table.csv", "r")
fixture_dict = list(csv.DictReader(file, delimiter=","))
file.close()

with open("master_table.csv", newline='') as file:
    game_list = list(csv.reader(file))

fixture_list = []
result_list = []

for x in range(len(game_list)):
    if game_list[x][8] == "not played":
        fixture_list.append(game_list[x])
    elif game_list[x][8] == "winner":
        fixture_list.append(game_list[x])
        result_list.append(game_list[x])
    else:
        result_list.append(game_list[x])

write_to_file("fixture_list.csv", fixture_list)
write_to_file("result_list.csv", result_list)
