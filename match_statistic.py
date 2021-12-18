from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


def match_result(href):
    driver.get(href)
    time.sleep(1)
    html = driver.page_source
    soup = BeautifulSoup(html, features='html.parser')
    teams = list(map(lambda x: x.find("div", class_="b-title bt16 bold").get_text(), soup.find_all("div", class_="team-name")))
    score = soup.find_all("div", class_="score")[2].find("div", class_="b-title bt16 bold").get_text().split(':')
    teams.append(score[0])
    teams.append(score[1])
    return teams


def all_matches_results(fileName, fileLinks):
    links = open("./dataset/" + fileLinks + '.txt', 'r').read().split('\n')
    f = open("./dataset/" + fileName + '.csv', 'w')
    titles = ('Team1', 'Team2', 'Score1', 'Score2')
    f.write(','.join(titles) + '\n')
    for link in links:
        f.write(','.join(match_result(link)) + '\n')
    f.close()


def assign_team_number(fileName, fileMatches):
    df = pd.read_csv("./dataset/" + fileMatches + '.csv')
    open("./dataset/" + fileMatches + '.txt', 'w').write('\n'.join(set(df['Team1']) | set(df['Team2'])))

def match_to_numbers(fileName, fileTeams, fileMatches):
    teams = open("./dataset/" + fileTeams + '.txt', 'r').read().split('\n')
    data = open("./dataset/" + fileMatches + '.csv', 'r').read().split('\n')[1:]
    file = open("./dataset/" + fileName + '.txt', "w")
    for item in data:
        text = item.split(',')
        team1 = teams.index(text[0])
        team2 = teams.index(text[1])
        for _ in range(int(text[2])):
            file.write(str(team1) + ',' + str(team2) + '\n')
        for _ in range(int(text[3])):
            file.write(str(team2) + ',' + str(team1) + '\n')
    file.close()

# all_matches_results('matches', 'links')
# assign_team_number("teams_list", "matches")
match_to_numbers('matches_list', 'teams_list', 'matches')

driver.close()
