from urllib.request import urlopen
from bs4 import BeautifulSoup


def veg_prices(url):
    raw_html = urlopen(url)
    html = BeautifulSoup(raw_html, 'html5lib')

    table = html.find('div', {'class': 'one_half'}).table.tbody.findAll('tr')
    veg_dict = dict()

    for row in table:
        veg_dict[row.findAll('td')[1].text.strip().lower()] = float(row.findAll('td')[2].text.strip()[4:])

    return veg_dict


if __name__ == '__main__':
    url = 'http://www.truetamil.in/price/vegetable-price-bangalore.php'
    dictionary = veg_prices(url)
    print(dictionary)

