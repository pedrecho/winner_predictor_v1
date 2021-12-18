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
    # print(score)
    teams.append(score[0])
    teams.append(score[1])
    return teams


def all_matches_results(fileName, fileLinks):
    links = open(fileLinks + '.txt', 'r').read().split('\n')
    f = open(fileName + '.txt', 'w')
    for link in links:
        f.write(','.join(match_result(link)) + '\n')
    f.close()


def assign_team_number(fileName, fileMatches):
    teams_number = []
    matches = open(fileMatches + '.txt', 'r').read().split('\n')
    for match in matches:
        teams_name = match.split(',')
        for i in range(2):
            if teams_name[i] not in teams_number:
                teams_number.append(teams_name[i])
    open(fileName + '.txt', "w").write("\n".join(teams_number))


def match_to_numbers(fileName):
    return

assign_team_number("teams_list", "matches")

driver.close()