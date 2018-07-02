from urllib.request import urlopen
from bs4 import BeautifulSoup


# Function to scrape vegetable prices from the web
def veg_prices(url):
    # Get the HTML and Parse it with Beautiful Soup
    raw_html = urlopen(url)
    html = BeautifulSoup(raw_html, 'html5lib')

    # Parse HTML and extract Information
    table = html.find('div', {'class': 'one_half'}).table.tbody.findAll('tr')
    veg_dict = dict()

    # Save all the Vegetable and their prices in the form of a dictionary
    for row in table:
        veg_dict[row.findAll('td')[1].text.strip().lower()] = float(row.findAll('td')[2].text.strip()[4:])

    return veg_dict


if __name__ == '__main__':
    # To visualize the Current prices, Print them on console
    url = 'http://www.truetamil.in/price/vegetable-price-bangalore.php'
    dictionary = veg_prices(url)
    print(dictionary)

