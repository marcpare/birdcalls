#
# There are 99 Common birds in April, May, June
# 49 of them are Flycatchers, Songbirds and Allies (Order Passeriformes)
# 13 of them are Shorebirds, Gulls, Auks and Allies (Order Charadriiformes)
#

from scrape_base import *
import re

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

def lookup(names):
    res = []
    for name in names:
        details = db_get('birds', name)
        res.append((name, details['family']))
    
    res = sorted(res, key=lambda x: x[1])
    
    anatidae = [
        "Ducks, Geese and Swans (Family Anatidae)"
    ]
    
    charadriiformes = [
         "Plovers (Family Charadriidae)",
         "Oystercatchers (Family Haematopodidae)",
         "Stilts and Avocets (Family Recurvirostridae)",
         "Sandpipers, Phalaropes and Allies (Family Scolopacidae)",
         "Gulls and Terns (Family Laridae)",
         "Skuas and Jaegers (Family Stercorariidae)",
         "Auks, Murres and Puffins (Family Alcidae)"
    ]
    
    passeriformes = [
        "Tyrant Flycatchers (Family Tyrannidae)",
        "Shrikes (Family Laniidae)",  
        "Vireos (Family Vireonidae)",  
        "Crows, Jays and Allies (Family Corvidae)",  
        "Larks (Family Alaudidae)",  
        "Swallows (Family Hirundinidae)",  
        "Chickadees (Family Paridae)",  
        "Bushtits (Family Aegithalidae)",  
        "Nuthatches (Family Sittidae)",  
        "Creepers (Family Certhiidae)",  
        "Wrens (Family Troglodytidae)",  
        "Dippers (Family Cinclidae)", 
        "Kinglets (Family Regulidae)",  
        "Gnatcatchers (Family Sylviidae)",  
        "Thrushes (Family Turdidae)",  
        "Mockingbirds, Thrashers and Allies (Family Mimidae)",  
        "Starlings (Family Sturnidae)",  
        "Accentors (Family Prunellidae)",  
        "Wagtails and Pipits (Family Motacillidae)",  
        "Waxwings (Family Bombycillidae)",  
        "Silky-flycatchers (Family Ptilogonatidae)",  
        "Warblers (Family Parulidae)",  
        "Tanagers (Family Thraupidae)",  
        "Sparrows, Towhees, Longspurs and Allies (Family Emberizidae)",  
        "Grosbeaks, Buntings and Allies (Family Cardinalidae)",  
        "Blackbirds and Allies (Family Icteridae)",  
        "Finches and Allies (Family Fringillidae)",  
        "Old World Sparrows (Family Passeridae)"
    ]
    
    for (bird, family) in res:
        if family not in charadriiformes and family not in passeriformes and family not in anatidae:
            print family
    
    

if __name__ == "__main__":
    freqs = scrape_freq_table()
    names = extract_common_species(freqs, [3, 4, 5])
    lookup(names)