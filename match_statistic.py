from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

def match_result(href):
    driver.get(href)
    time.sleep(1)
    html = driver.page_source
    soup = BeautifulSoup(html, features='html.parser')
    teams = list(map(lambda x: x.find("div",class_="b-title bt16 bold").get_text(), soup.find_all("div",class_="team-name")))
    score = soup.find_all("div", class_="score")[2].find("div",class_="b-title bt16 bold").get_text().split(':')
    teams.append(score[0])
    teams.append(score[1])
    return teams

def all_matches_results():
    links = open('links2.txt', 'r').read().split('\n')
    f = open('matches_result.txt','w')
    for link in links:
        f.write('; '.join(match_result(link)))
    f.close()

