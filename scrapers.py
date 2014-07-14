from bs4 import BeautifulSoup
import re

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