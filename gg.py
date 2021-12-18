from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import datetime
import copy

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


def to_normal_date(s: datetime.date):
    return str(s.day) + '.' + str(s.month) + '.' + str(s.year)


def get_links(filename, firstDate, lastDate=datetime.datetime.now().date()):
    links = []
    deltaDate = datetime.timedelta(days=1)
    lastDate -= deltaDate
    currentDate = firstDate
    while currentDate <= lastDate:
        driver.get("https://cyberscore.live/matches/?date=" + to_normal_date(currentDate))
        time.sleep(1)
        while len(driver.find_elements(By.CSS_SELECTOR, "div.load-more")) > 0:
            driver.find_elements(By.CSS_SELECTOR, "div.load-more")[0].click()
            time.sleep(1)
        html = driver.page_source
        soup = BeautifulSoup(html, features='html.parser')
        items = soup.find_all('a', class_="item info-blocks-item-height")
        for item in items:
            href = item.get('href')
            if href != '':
                links.append("https://cyberscore.live" + item.get('href'))
        currentDate += deltaDate
    open(filename + '.txt', 'w').write('\n'.join(links))


def find_all_heroes():
    url = "https://ru.dotabuff.com/heroes"
    driver.get(url)
    time.sleep(1)
    html = driver.page_source
    soup = BeautifulSoup(html, features='html.parser')
    list_a = soup.find("div", class_="hero-grid").find_all("a")
    return list(map(lambda x: x.get("href").split("/")[-1].replace("-", "_"), list_a))


def get_hero_list(filename):
    driver.get("https://liquipedia.net/dota2/Cheats")
    time.sleep(1)
    html = driver.page_source
    soup = BeautifulSoup(html, features='html.parser')
    items = list(map(lambda x: x.text.strip('\n').lower(),
                     soup.find('span', id='Hero_Names').parent.parent.find('table').find_all('td')))
    heroes = find_all_heroes()
    oldHeroes = list(map(lambda x: x.replace(' ', '_').replace('-', '_').replace('\'', ''), items[0::2]))
    exHeroes = ['outworld_destroyer']
    for hero in heroes:
        if hero not in oldHeroes and hero not in exHeroes:
            items.append(hero)
            items.append(hero)
    items = list(map(lambda x: x.split(' ')[-1], items[1::2]))
    open(filename + '.txt', 'w').write('\n'.join(items))


def team_win_rate(team):
    driver.get("https://ru.dotabuff.com/")
    time.sleep(1)
    driver.find_elements(By.ID, "q")[1].send_keys(team)
    driver.find_element(By.NAME, "button").click()
    time.sleep(1)
    driver.find_element(By.CLASS_NAME, "result-team").click()
    time.sleep(1)
    html = driver.page_source
    soup = BeautifulSoup(html, features="html.parser")
    return int(float(soup.find_all("table", class_="table-striped")[2].find("tbody").find_all("tr")[0].find_all("td")[2].get("data-value")))/100


def find_statistic(href):
    driver.get(href)
    time.sleep(1)
    html = driver.page_source
    soup = BeautifulSoup(html, features='html.parser')
    team_names = list(map(lambda x: x.find("div",class_="b-title bt16 bold").get_text(), soup.find_all("div",class_="team-name")))
    massiv = []
    maps_href = list(
        map(lambda x: "https://cyberscore.live" + x.get('href'), soup.find("div", class_="tab-controls").find_all("a")))
    for map_href in maps_href:
        driver.get(map_href)
        time.sleep(1)
        html = driver.page_source
        soup = BeautifulSoup(html, features='html.parser')
        player_list = soup.find_all("div", class_="item-bottom-player help")
        images = list(map(lambda x: x.find("img"), player_list))
        if None not in images:
            images_src = list(map(lambda x: x.get("src"), images))
            item_team_1 = soup.find("div", class_="item team-1")
            images_src.append(item_team_1.find("div", class_="winner-icon") is not None)
            if len(images_src) == 11:
                massiv.append(copy.deepcopy(images_src))
        time.sleep(1)
    team_winrate1 = team_win_rate(team_names[0])
    time.sleep(1)
    team_winrate2 = team_win_rate(team_names[1])
    for item in massiv:
        item.append(team_winrate1)
        item.append(team_winrate2)
    return massiv

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

def hero_name(href):
    return href.replace("https://s.cyberscore.live/wp-content/uploads/2021/09/hero-", "").replace(
        "-image-2021-95x70.png", "")


def read_games(fileData, fileLinks, fileHeroes, add=True):
    links = open(fileLinks + '.txt', 'r').read().split('\n')
    heroes = open(fileHeroes + '.txt', 'r').read().split('\n')
    if not add:
        title = 'r_' + ',r_'.join(heroes) + ',d_' + ',d_'.join(heroes) + ',win\n'
        open(fileData + '.csv', 'w').write(title)
    for link in links:
        statistics = find_statistic(link)
        for item in statistics:
            print(item)
            for i in range(10):
                item[i] = hero_name(item[i])
                if item[i] in heroes:
                    item[i] = heroes.index(item[i])
                else:
                    print(item[i])
            record = ['0'] * 2 * len(heroes)
            for i in range(10):
                if i < 5:
                    record[item[i]] = '1'
                else:
                    record[item[i] + len(heroes)] = '1'
            record.append(str(item[10]))
            open(fileData + '.csv', 'a').write(','.join(record) + '\n')


# get_hero_list('heroes')
# get_links('links4', datetime.date.fromisoformat('2021-09-26'), datetime.date.fromisoformat('2021-10-29'))
# read_games('data', 'links4', 'heroes')
driver.close()
