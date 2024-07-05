import sys
import os
import argparse
import time
import random
import requests
from bs4 import BeautifulSoup
import logging
import re
from dotenv import load_dotenv
from tqdm import tqdm
from colorama import Fore, Style
from app.selenium import driver, actions, By, Keys, stealth


load_dotenv()
SCRAPPING_TITLE = os.getenv("SCRAPPING_TITLE")
SCRAPPING_BASE_URL = os.getenv("SCRAPPING_BASE_URL")
STARTING_PAGE = os.getenv("STARTING_PAGE")
A_TAG_CLASS = os.getenv("A_TAG_CLASS")
DOWNLOAD_URL = os.getenv("DOWNLOAD_URL")
SCRAPPING_PRE_PAGE_PARAM = os.getenv("SCRAPPING_PRE_PAGE_PARAM")
SCRAPPING_POST_PAGE_PARAM = os.getenv("SCRAPPING_POST_PAGE_PARAM")
IS_CLOUDFLARE = os.getenv("IS_CLOUDFLARE")


start_time = time.strftime('%Y%m%d_%H%M')
# 로그 메시지의 형식을 설정합니다.
log_format = "%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s"

# 로그 설정을 초기화합니다.
logging.basicConfig(
    filename=f"[{SCRAPPING_TITLE}]app.log", level=logging.DEBUG, format=log_format)


def webscraping_using_requests():
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
    }
    flag = True
    page = int(STARTING_PAGE)

    while flag:
        try:
            print(Fore.BLUE + Style.BRIGHT + 'INFO:' +
                  Style.RESET_ALL + f' page {page}')
            logging.info(f'page {page}')
            base_url = SCRAPPING_BASE_URL
            url = base_url + SCRAPPING_PRE_PAGE_PARAM + \
                str(page) + SCRAPPING_POST_PAGE_PARAM

            session = requests.Session()
            session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
                'Accept': 'text/html, */*; q=0.01',
                'Accept-Language': 'en-US,en;q=0.5',
                'Referer': 'https://www.thelancet.com/action/doSearch?',
                'X-Requested-With': 'XMLHttpRequest',
                'Origin': 'https://www.thelancet.com',
                'Connection': 'keep-alive',
            })
            if IS_CLOUDFLARE == 'True':
                scraper = cloudscraper.create_scraper(
                    debug=True, browser={'browser': 'firefox', 'platform': 'windows', 'mobile': False})
                response = scraper.get(url)
                print(response.content)
            else:
                response = session.get(url)
                print(response.text)

            soup = BeautifulSoup(response.text, 'html.parser')
            if response.status_code != 200:
                print(Fore.RED + 'ERROR:' + Style.RESET_ALL, response.status_code)
                logging.error(f'{response.status_code}')
                flag = False
                break

            link_a_tags = soup.find_all(
                'a', {'class': re.compile(fr'{A_TAG_CLASS}.*')})

            links = []
            for i in range(len(link_a_tags)-1):
                links.append(base_url + link_a_tags[i].get(DOWNLOAD_URL))
            if len(links) == 0:
                print(Fore.RED + 'ERROR:' + Style.RESET_ALL +
                      ' No links found in the page')
                logging.error('No links found in the page')
                flag = False
                break
            for link in links:
                response = requests.get(
                    link, headers=headers, stream=True, allow_redirects=True)
                if (response.status_code != 200):
                    print(Fore.RED + 'ERROR:' +
                          Style.RESET_ALL, response.status_code)
                    logging.error(f'{response.status_code}')
                else:
                    title = link.split('/')[-1].split('?')[0]
                    with open(f'./data/{title}', 'wb') as file:
                        print(Fore.GREEN + 'INFO:' + Style.RESET_ALL +
                              f' Downloading {title}')
                        logging.info(f'Downloading {title}')
                        for data in tqdm(iterable=response.iter_content(chunk_size=1024), total=int(response.headers.get('content-length', 0))//1024, unit='KB'):
                            file.write(data)
                        print(Fore.GREEN + 'INFO:' + Style.RESET_ALL +
                              f' Download Complete {title}')
                        logging.info(f'Download Complete {title}')
                    time.sleep(random.randint(1, 10)/10)
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            fname = os.path.split(exc_traceback.tb_frame.f_code.co_filename)[1]
            print(Fore.RED + 'ERROR:' + Style.RESET_ALL, e)
            print(Fore.RED + 'ERROR:' + Style.RESET_ALL + ' Filename ', fname)
            print(Fore.RED + 'ERROR:' + Style.RESET_ALL + ' Type ', exc_type)
            print(Fore.RED + 'ERROR:' + Style.RESET_ALL +
                  ' Line_number ', exc_traceback.tb_lineno)
            logging.error(f'{e}')
            logging.error(f'\tFilename {fname}')
            logging.error(f'\tType {exc_type}')
            logging.error(f'\tLine_number {exc_traceback.tb_lineno}')
            flag = False
            print(Style.RESET_ALL)
            break

        page += 1


def webscraping_using_selenium():
    flag = True
    page = int(STARTING_PAGE)
    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )

    while flag:
        try:
            print(Fore.BLUE + Style.BRIGHT + 'INFO:' +
                  Style.RESET_ALL + f' page {page}')
            logging.info(f'page {page}')
            base_url = SCRAPPING_BASE_URL
            url = base_url + SCRAPPING_PRE_PAGE_PARAM + \
                str(page) + SCRAPPING_POST_PAGE_PARAM

            driver.get(url)
            time.sleep(5)
            try:
                cookie_modal_button = driver.find_element(
                    By.ID, 'onetrust-accept-btn-handler')
                cookie_modal_button.click()
                time.sleep(2)
            except:
                print('No cookie modal found')
            try:
                register_modal_button = driver.find_element(
                    By.CLASS_NAME, 'featherlight-close-icon featherlight-close')
                register_modal_button.click()
                time.sleep(2)
            except:
                print('No register modal found')

            links = driver.find_elements(By.CLASS_NAME, A_TAG_CLASS)
            if len(links) == 0:
                print(Fore.RED + 'ERROR:' + Style.RESET_ALL +
                      ' No links found in the page')
                logging.error('No links found in the page')
                flag = False
                break
            for link in links:
                print(link.get_attribute('href'))
                actions.context_click(link).perform()
                actions.send_keys(Keys.ARROW_DOWN).send_keys(
                    Keys.ARROW_DOWN).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ENTER).perform()
                time.sleep(2)
                time.sleep(random.randint(1, 10)/10)
            else:
                input('Press Enter to continue...')
                tabs = driver.window_handles
                for tab in tabs[1:]:
                    driver.switch_to.window(tab)
                    driver.refresh()
                    time.sleep(2)
                    driver.close()
                driver.switch_to.window(tabs[0])

        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            fname = os.path.split(exc_traceback.tb_frame.f_code.co_filename)[1]
            print(Fore.RED + 'ERROR:' + Style.RESET_ALL, e)
            print(Fore.RED + 'ERROR:' + Style.RESET_ALL + ' Filename ', fname)
            print(Fore.RED + 'ERROR:' + Style.RESET_ALL + ' Type ', exc_type)
            print(Fore.RED + 'ERROR:' + Style.RESET_ALL +
                  ' Line_number ', exc_traceback.tb_lineno)
            logging.error(f'{e}')
            logging.error(f'\tFilename {fname}')
            logging.error(f'\tType {exc_type}')
            logging.error(f'\tLine_number {exc_traceback.tb_lineno}')
            flag = False
            print(Style.RESET_ALL)
            break
        page += 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--selenium', action='store_true')

    args = parser.parse_args()

    if args.selenium:
        webscraping_using_selenium()
    else:
        webscraping_using_requests()
