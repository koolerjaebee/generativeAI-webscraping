import time
import random
import requests
from bs4 import BeautifulSoup

flag = True
while flag:

    page = 1
    base_url = 'https://jamanetwork.com'
    url = base_url + f'/searchresults?q=clinical&f_ArticleTypeDisplayName=Research&exPrm_qqq=%7bDEFAULT_BOOST_FUNCTION%7d%22clinical%22&exPrm_hl.q=clinical&page={page}&f_OpenAccessFilter=true'
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})

    soup = BeautifulSoup(response.text, 'html.parser')
    if response.status_code != 200:
        print('Error:', response.status_code)
        break

    # # Example of page
    # html_example = soup.prettify("utf-8")
    # with open("example.html", "wb") as file:
    #     file.write(html_example)

    title_h3_tags = soup.find_all('h3', {'class': 'article--title at-sr-item-title-link'})
    link_a_tags = soup.find_all('a', {'class': 'al-link pdf pdfaccess'})

    pdfs = []
    for i in range(len(title_h3_tags)):
        pdfs.append({'title': title_h3_tags[i].text, 'link': base_url + link_a_tags[i].get('data-article-url')})

    for pdf in pdfs:
        with open(f'./data/{pdf["title"]}.pdf', 'wb') as file:
            response = requests.get(pdf['link'], headers={'User-Agent': 'Mozilla/5.0'})
            file.write(response.content)
            print(f'{pdf["title"]} downloaded')
            time.sleep(random.randint(1, 3))

    page += 1
