from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import argparse

URL = "https://cariboutests.com/games/skyscrapers.php"

def process_header_tr(tr):
    return [int(td.text) for td in tr.find_all("td")[1:-1]]

def process_middle_tr(tr):
    tds = tr.find_all('td')
    left = tds[0].div.span.text
    right = tds[-1].div.span.text
    return [int(left), int(right)]

def process_page(source):
    soup = BeautifulSoup(source, 'html.parser')
    problem = soup.find(id='sky')
    table = problem.table.tbody
    trs = table.find_all('tr')
    results = []
    for index,tr in enumerate(trs):
        if index == 0:
            results.append(process_header_tr(tr))
        elif index == len(trs)-1:
            results.append(process_header_tr(tr))
        else:
            results.append(process_middle_tr(tr))
    return results

def download_page(board_size):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.goto(URL, wait_until="load")
        page.select_option("select", value=str(board_size))
        page.click("input[type=submit]")
        page.wait_for_load_state("load")
        src = page.content()
        browser.close()
        return src

def run():
    parser = argparse.ArgumentParser(description='Download sky scraper problems')

    parser.add_argument('--board_size', '-b', type=int, help='Size of board to download', default=6)
    parser.add_argument("--out_file", "-o", help="File to write the problem to", default="skyscraper_problem.txt")

    args = parser.parse_args()

    with open(args.out_file, "w") as file:
        file.write("BOARD_SIZE:\t" + str(args.board_size) + '\n')
        file.write('\n')
        results = process_page(download_page(args.board_size))
        for result in results:
            for data in result:
                file.write(str(data) + "\t")
            file.write('\n')

if __name__ == "__main__":
    run()