import sys, os
import time
import random
import requests
from bs4 import BeautifulSoup
import logging
import re
from dotenv import load_dotenv


load_dotenv()
SCRAPPING_TITLE = os.getenv("SCRAPPING_TITLE")
SCRAPPING_BASE_URL = os.getenv("SCRAPPING_BASE_URL")
STARTING_PAGE = os.getenv("STARTING_PAGE")
A_TAG_CLASS = os.getenv("A_TAG_CLASS")
DOWNLOAD_URL = os.getenv("DOWNLOAD_URL")


start_time = time.strftime('%Y%m%d_%H%M')
logging.basicConfig(format='%(levelname)s | %(asctime)s | %(message)s', datefmt='%Y/%m/%d %I:%M:%S %p', filename=f'logs/{SCRAPPING_TITLE}_{start_time}.log', level=logging.INFO)


headers = {
    'user-agent': 'Mozilla/5.0 (Linux; Android 8.0.0; SM-G955U Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Mobile Safari/537.36'
}
flag = True
page = STARTING_PAGE


while flag:
    try:
        print(f'page: {page}')
        logging.info(f'page: {page}')
        base_url = SCRAPPING_BASE_URL
        url = base_url + f'/searchresults?q=clinical&f_ArticleTypeDisplayName=Research&exPrm_qqq=%7bDEFAULT_BOOST_FUNCTION%7d%22clinical%22&exPrm_hl.q=clinical&page={page}&f_OpenAccessFilter=true'
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})

        soup = BeautifulSoup(response.text, 'html.parser')
        if response.status_code != 200:
            print('Error:', response.status_code)
            logging.error(f'Error: {response.status_code}')
            flag = False
            break

        link_a_tags = soup.find_all('a', {'class': re.compile(fr'{A_TAG_CLASS}.*')})

        links = []
        for i in range(len(link_a_tags)-1):
            links.append(base_url + link_a_tags[i].get(DOWNLOAD_URL))
        for link in links:
            response = requests.get(link, headers=headers, stream=True, allow_redirects=True)
            if(response.status_code != 200):
                print('Error:', response.status_code)
                logging.error(f'Error: {response.status_code}')
            else:
                title = link.split('/')[-1].split('?')[0]
                with open(f'./data/{title}', 'wb') as file:
                    print(f'Downloading: {title}')
                    logging.info(f'Downloading: {title}')
                    file.write(response.content)
                print(f'Download Complete: {title}')
                logging.info(f'Download Complete: {title}')

                time.sleep(random.randint(1, 10)/10)
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        fname = os.path.split(exc_traceback.tb_frame.f_code.co_filename)[1]
        print('Error:', e)
        print('Error filename:', fname)
        print('Error type:', exc_type)
        print('Error line number:', exc_traceback.tb_lineno)
        logging.error(f'Error: {e}')
        logging.error(f'Error filename: {fname}')
        logging.error(f'Error type: {exc_type}')
        logging.error(f'Error line number: {exc_traceback.tb_lineno}')
        flag = False
        break

    page += 1
