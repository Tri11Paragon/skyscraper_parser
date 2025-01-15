from bs4 import BeautifulSoup
import subprocess
from selenium import webdriver
from requests_html import HTMLSession
# from seleniumrequests import Firefox
import time

URL = "https://cariboutests.com/games/skyscrapers.php"


def process_header_tr(tr):
    for td in tr.find_all('td')[1:-1]:
        print (f"header number: {td.div.span.text}")

def process_middle_tr(tr):
    tds = tr.find_all('td')
    left = tds[0].div.span.text
    right = tds[-1].div.span.text
    print (f"left: {left}, right: {right}")

def process_page(source):
    soup = BeautifulSoup(source, 'html.parser')
    problem = soup.find(id='sky')
    table = problem.table.tbody
    trs = table.find_all('tr')
    for index,tr in enumerate(trs):
        if index == 0:
            process_header_tr(tr)
        elif index == len(trs)-1:
            process_header_tr(tr)
        else:
            process_middle_tr(tr)

def download_page():
    subprocess.run(["curl", "-X", "POST", "--user-agent", "Mozilla/5.0 (X11; Linux x86_64; rv:131.0) Gecko/20100101 Firefox/131.0", "-d", "board_size: 8", "-o", "skyscrapers.php", URL])
    with open("skyscrapers.php", "r+") as file:
        content = file.read()
    # subprocess.run(["rm", "skyscrapers.php"])
    print(content)
    return content
    # options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    # driver = webdriver.Chrome(options=options)

    # session = HTMLSession()
    # r = session.post(url=URL, data={"board_size": "6"}, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:131.0) Gecko/20100101 Firefox/131.0"})
    # r.html.render()
    # print(r.html.find(id='sky'))
    # print(r.text)

    # print(driver.page_source)

    # post(driver, "6")
    # driver.get(URL)

    # src = driver.page_source
    # print(src)
    # driver.quit()

    # return r.text

if __name__ == "__main__":
    process_page(download_page())