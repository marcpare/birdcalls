# Pulling lots of data to study from -- 
# 
# http://www.birdweb.org/birdweb/birds
# 
# Be nice and cache the html once we've looked at it once
#
# Builds 
# families.json << python scrape.py families > families.json
# families/ << python scrape.py birds
# birds/ << python scrape.py bird
#
# ls -l birds | wc -l
# >> 492 # There are 492 bird species in Washington!
#   

from bs4 import BeautifulSoup
import os
import os.path
import sys
import json
from cache import *
import argparse as ap
from urlparse import urlparse, parse_qs

DEBUG = False

def get_soup(url):
    html = cached_request(url)
    return BeautifulSoup(html)

def prefixed_links(soup, prefix):
    # extract href and link string
    links = [(link.get("href"), link.string) for link in soup.find_all("a")]
    # filter empty links
    links = [(href, string) for (href, string) in links if href and href.startswith(prefix)]
    return links
    
def build_families_list():
    soup = get_soup('http://www.birdweb.org/birdweb/birds')    
    family_links = prefixed_links(soup, 'http://birdweb.org/birdweb/family/')

    families_json = [
        {
            'url': url,
            'family': family
        } for (url, family) in family_links if url
    ]
    
    print json.dumps(families_json)

def scrape_family(url):
    soup = get_soup(url)    
    family_links = prefixed_links(soup, 'http://birdweb.org/birdweb/bird/')
    
    family_json = [
        {'url': url} for (url, string) in family_links
    ]
    return family_json

def scrape_species_image(soup):
    """ Expects the link in the filmstrip that has data-contributor """
    small_img = soup.find("img")
    image_soup = get_soup(soup.get("data-image_url"))
    return {
        "src": image_soup.find("img").get("src"),
        "contributor": small_img.get("data-contributor"),
        "contributor_url": small_img.get("data-contributor_url")
    }

def scrape_species_images(soup):
    image_links = soup.find(id="filmstripscroll").find_all("a")
    return [scrape_species_image(link) for link in image_links]

def scrape_call(soup):
    button = soup.find(id="sound_button")
    # sometimes there is no call
    if button:
        call_player_url = button.get('data')
        # call url is embedded in a query string!
        query = urlparse(call_player_url).query
        qs = parse_qs(query)
        return qs['song_url'][0]
    return False

def scrape_species(url):
    soup = get_soup(url)
    
    species = {
        'common_name': soup.find(id="commonname").text.strip(),
        'images': scrape_species_images(soup),
        'call': scrape_call(soup)
    }
    
    return species
    
def species_scrape_test():
    scrape_species('http://birdweb.org/birdweb/bird/canada_goose')

def family_scrape_test():
    print scrape_family('http://birdweb.org/birdweb/family/anatidae')

def build_bird_lists(families_json):
    families = []
    for family in families_json:
        family['species'] = scrape_family(family['url'])
        db_add('families', family['short_name'], family)
 
def populate_bird_details():
    for family_name in db_list('families'):
        family = db_get('families', family_name)
        for species_json in family['species']:
            bird = scrape_species(species_json['url'])
            bird['family'] = family['family']
            short_name = species_json['url'].split('/')[-1]
            db_add('birds', short_name, bird)
    
if __name__ == '__main__':
    
    commands = {
        'families': build_families_list,
        'birds': build_bird_lists,
        'bird': populate_bird_details,
        'family_scrape_test': family_scrape_test,
        'species_scrape_test': species_scrape_test
    }
    
    def main(command, filename=None):
        if filename:
            json_data = json.loads(open(filename).read())
            commands[command](json_data)
        else:
            commands[command]()
        
    parser = ap.ArgumentParser()
    parser.add_argument('command', choices=commands.keys())
    parser.add_argument('filename', nargs='?')
    args = parser.parse_args()
    
    main(**vars(args))
    






