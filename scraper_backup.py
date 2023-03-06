import requests
import csv
import re
from bs4 import BeautifulSoup
from links import urls


def scrape_time():
    response = requests.get('https://www.footywire.com/afl/footy/supercoach_prices')
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')
    table = soup.find("div", {"id": "fantasy-prices-div"}).find('table', {"width": "998"})
    rows = table.find_all('tr')
    rows.pop(0)

    # data = []
    names = []
    for row in rows:
        # player_data = row.find_all('td')
        # name = player_data[0].text.strip()
        # price = player_data[1].text.strip()
        # data.append([name, price])
        player_data = row.find_all('td')
        name = player_data[0].text.strip()
        names.append(name[1:].lower().strip())

    # with open('players.csv', 'w') as f:
    #     write = csv.writer(f)
    #     write.writerow(['Name', 'Price'])
    #     write.writerows(data)

    request = requests.get('https://www.google.com.au/search?q=supercoach+2023+players').text
    soup = BeautifulSoup(request, 'html.parser')
    url_list = []
    for link in soup.find_all("a",href=re.compile("(?<=/url\?q=)(htt.*://.*)")):
        url_list.append(re.split(":(?=http)",link["href"].replace("/url?q=","")))

    frequency_dict = {}
    for url in url_list:
        request = requests.get(url).text
        soup = BeautifulSoup(request, 'html.parser')
        text = soup.get_text().lower()
        for word in names:
            freq = text.count(word)
            if freq != 0:
                frequency_dict[word] = frequency_dict.get(word, 0) + freq
            
    print(frequency_dict)
