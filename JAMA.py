import time
import random
import requests
from bs4 import BeautifulSoup


headers = {
    'user-agent': 'Mozilla/5.0 (Linux; Android 8.0.0; SM-G955U Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Mobile Safari/537.36'
}

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
        pdfs.append({'title': title_h3_tags[i].text.strip().replace('\n', ' '), 'link': base_url + link_a_tags[i].get('data-article-url')})
    for pdf in pdfs:
        response = requests.get(pdf['link'], headers=headers, stream=True, allow_redirects=True)
        if(response.status_code != 200):
            print('Error:', response.status_code)
        else:
            with open(f'./data/{pdf["title"]}.pdf', 'wb') as file:
                print(f'Downloading {pdf["title"]}')
                file.write(response.content)
            # with open(f'./data/{pdf["title"]}.txt', 'a') as file:
            #     file.write(str(response.text))
            print(type(response.content))
            print(str(response.content)[:1000])
            print('='*150)
            print(str(response.content)[-1000:])
            print(f'{pdf["title"]} downloaded\n')

            time.sleep(random.randint(1, 3))

    page += 1
