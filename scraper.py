import requests
import re
from bs4 import BeautifulSoup
import url_searches


def scrape_time():
    # retreieve all supercoach player names
    response = requests.get('https://www.footywire.com/afl/footy/supercoach_prices')
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')
    table = soup.find("div", {"id": "fantasy-prices-div"}).find('table', {"width": "998"})
    rows = table.find_all('tr')
    rows.pop(0)

    player_dict = {}
    names = []
    for row in rows:
        player_data = row.find_all('td')
        name = player_data[0].text.strip()
        name_short = name[2:].lower()
        price = player_data[1].text.strip()
        names.append(name_short)
        player_dict[name_short] = {}
        player_dict[name_short]['price'] = price
    

    # search google for supercoach pages
    for url in url_searches.searches:
        request = requests.get(url).text
        soup = BeautifulSoup(request, 'html.parser')
        url_list = []
        for link in soup.find_all("a",href=re.compile("(?<=/url\?q=)(htt.*://.*)")):
            url_ending = link["href"].find('&sa')
            url_list.append(re.split(":(?=http)",link["href"][0:url_ending].replace("/url?q=","")))

    # find the frequency of the player's names on the pages
    for url in url_list:
        try:
            request = requests.get(url[0]).text
        except requests.exceptions.RequestException:
            pass
        soup = BeautifulSoup(request, 'html.parser')
        text = soup.get_text().lower()
        for word in names:
            freq = text.count(word)
            if freq != 0:
                player_dict[word]['frequency'] = player_dict.get(word, 0).get('frequency', 0) + freq


    print(player_dict)