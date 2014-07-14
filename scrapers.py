from bs4 import BeautifulSoup
import re
from urlparse import urlparse
from cgi import parse_qs

# Scrape the frequency checklist on birdweb.org
# http://www.birdweb.org/birdweb/ecoregion/sites/puget_trough/site
def scrape_checklist(content):
    soup = BeautifulSoup(content)
    table = soup.find(id="concern").table    
    frequencies = {}
    for (index, row) in enumerate(table.children):
        # skip first two rows
        if index <= 1:
            continue
        
        freq = []
        for cell in row.children:
            if cell.name == 'th':
                species = cell.string
            else:
                freq.append(cell.text)
        frequencies[species] = freq
        
    return frequencies

class BirdWebScraper(object):
    def __init__(self, requester):
        self.requester = requester

    # Scrape birdweb species page
    # http://www.birdweb.org/birdweb/bird/red_knot
    def scrape_species_birdweb(self, content):
        soup = BeautifulSoup(content)
        species = {
            'common_name': soup.find(id="commonname").text.strip(),
            'images': self.scrape_species_images(soup),
            'call': self.scrape_call(soup)
        }
        return species

    def scrape_species_image(self, soup):
        """ Expects the link in the filmstrip that has data-contributor """
        small_img = soup.find("img")
        image_soup = BeautifulSoup(self.requester(soup.get("data-image_url")))
                
        return {
            "src": image_soup.find("img").get("src"),
            "contributor": small_img.get("data-contributor"),
            "contributor_url": small_img.get("data-contributor_url")
        }

    def scrape_species_images(self, soup):
        image_links = soup.find(id="filmstripscroll").find_all("a")
        return [self.scrape_species_image(link) for link in image_links]

    def scrape_call(self, soup):
        button = soup.find(id="sound_button")
        # sometimes there is no call
        if button:
            call_player_url = button.get('data')
            # call url is embedded in a query string!
            query = urlparse(call_player_url).query
            qs = parse_qs(query)
            return qs['song_url'][0]
        return False

