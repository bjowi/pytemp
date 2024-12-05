from bs4 import BeautifulSoup

def parse_aro(html):

    soup = BeautifulSoup(html, 'html.parser')

    stations = {}
    for row in soup.find_all(class_="tor-link-text-row"):
        items = row.find_all(class_="tor-link-text-row-item")
        ki, vi = items
        if ki.text:
            stations[ki.text] = vi.text

    return stations
