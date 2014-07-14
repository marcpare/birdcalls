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

class AllAboutBirdsScraper(object):
    def __init__(self, requester):
        self.requester = requester
    
    def species(self, name):
        url = "http://www.allaboutbirds.org/guide/%s/id" % name
        content = self.requester(url)
        ret = self.scrape_species(content)
        
        url = "http://www.allaboutbirds.org/guide/%s/lifehistory" % name
        content = self.requester(url)
        ret.update(self.scrape_life_history(content))
        
        return ret
    
    def scrape_species(self, content):
        soup = BeautifulSoup(content)
        return {
            'description': soup.find(id='id_keys').text
        }
    
    def scrape_life_history(self, content):
        soup = BeautifulSoup(content)
        
        ret = {}
        
        habitat = soup.find(href='#at_habitat')
        if habitat:
            ret['habitat'] = habitat.text
        
        cool_facts = soup.find(id='life_coolfacts')
        if cool_facts:
            ret['cool_facts'] = cool_facts.text
        
        return ret
    
class BirdWebScraper(object):
    def __init__(self, requester):
        self.requester = requester

    def species(self, name):
        url = "http://www.birdweb.org/birdweb/bird/%s" % name
        content = self.requester(url)
        return self.scrape_species(content)

    # Scrape birdweb species page
    # http://www.birdweb.org/birdweb/bird/red_knot
    def scrape_species(self, content):
        soup = BeautifulSoup(content)
        species = {
            'common_name': soup.find(id="commonname").text.strip(),
            'images': self.scrape_species_images(soup),
            'call': self.scrape_call(soup),
            'description': self.scrape_description(soup),
            'life_history': self.scrape_life_history(soup)
        }
        return species
    
    def scrape_description(self, soup):
        return soup.find(id='description').text
        
    def scrape_life_history(self, soup):
        return soup.find(id='life_history').text
    
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

