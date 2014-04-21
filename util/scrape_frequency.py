#
# There are 99 Common birds in April, May, June
# 49 of them are Flycatchers, Songbirds and Allies (Order Passeriformes)
# 13 of them are Shorebirds, Gulls, Auks and Allies (Order Charadriiformes)
#
# build list of songbirds:
# python scrape_frequency.py passeriformes1 > ../data/passeriformes1.json
# python scrape_frequency.py passeriformes2 > ../data/passeriformes2.json
# python scrape_frequency.py passeriformes3 > ../data/passeriformes3.json
# python scrape_frequency.py passeriformes4 > ../data/passeriformes4.json

from scrape_base import *
import re

groups = {
    'anatidae': [
        "Ducks, Geese and Swans (Family Anatidae)"
    ],
    'charadriiformes': [
         "Plovers (Family Charadriidae)",
         "Oystercatchers (Family Haematopodidae)",
         "Stilts and Avocets (Family Recurvirostridae)",
         "Sandpipers, Phalaropes and Allies (Family Scolopacidae)",
         "Gulls and Terns (Family Laridae)",
         "Skuas and Jaegers (Family Stercorariidae)",
         "Auks, Murres and Puffins (Family Alcidae)"
    ],
    'passeriformes1': [
        "Tyrant Flycatchers (Family Tyrannidae)",
        "Shrikes (Family Laniidae)",  
        "Vireos (Family Vireonidae)",  
        "Crows, Jays and Allies (Family Corvidae)",  
        "Larks (Family Alaudidae)",  
        "Swallows (Family Hirundinidae)",  
        "Chickadees (Family Paridae)"
    ],
    'passeriformes2': [  
        "Warblers (Family Parulidae)",  
        "Bushtits (Family Aegithalidae)",  
        "Nuthatches (Family Sittidae)",  
        "Creepers (Family Certhiidae)",  
        "Wrens (Family Troglodytidae)",  
        "Dippers (Family Cinclidae)",
        "Waxwings (Family Bombycillidae)",  
        "Silky-flycatchers (Family Ptilogonatidae)"
    ],
    'passeriformes3': [ 
        "Kinglets (Family Regulidae)",  
        "Gnatcatchers (Family Sylviidae)",  
        "Thrushes (Family Turdidae)",  
        "Mockingbirds, Thrashers and Allies (Family Mimidae)",  
        "Starlings (Family Sturnidae)",  
        "Accentors (Family Prunellidae)",
        "Wagtails and Pipits (Family Motacillidae)"
    ],
    'passeriformes4': [  
        
        "Tanagers (Family Thraupidae)",  
        "Sparrows, Towhees, Longspurs and Allies (Family Emberizidae)",  
        "Grosbeaks, Buntings and Allies (Family Cardinalidae)",  
        "Blackbirds and Allies (Family Icteridae)",  
        "Finches and Allies (Family Fringillidae)",  
        "Old World Sparrows (Family Passeridae)"
    ]
}

def scrape_freq_table():
    soup = get_soup('http://www.birdweb.org/birdweb/ecoregion/sites/puget_trough/site')
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
    
def extract_common_species(frequencies, months=[]):
    names = []
    for (species, freqs) in frequencies.items():
        fs = [freqs[mi] for mi in months]
        if any([f == 'C' for f in fs]):
            names.append(short_name(species))
    return names

def short_name(long_name):
    s = long_name.lower().replace(' ', '_')
    return re.sub('[^a-z_-]', '', s)

def print_group_list(group):
    freqs = scrape_freq_table()
    names = extract_common_species(freqs, [3, 4, 5])
    
    bird_details = [db_get('birds', name) for name in names]
    group_list = [bd for bd in bird_details if bd['family'] in group]
    
    #short_names = [short_name(bd['common_name']) for bd in group_list]
    
    print json.dumps(group_list)

if __name__ == "__main__":    
    
    def main(group):
        print_group_list(groups[group])
        
    parser = ap.ArgumentParser()
    parser.add_argument('group', choices=groups.keys())
    args = parser.parse_args()
    
    main(**vars(args))
    
    
    
    
    
    
    
    