#!/usr/bin/env python

cmd_doc = """
Commands:

checklist           Print the checklist(s)
scrape_checklist    Uses the checklist url and scrape the frequency table
populate_checklist  scrapes then fills in the db
birds_in [checklist] [Jan, Feb, ...] [frequency]    prints the birds at this place, time, and freqency

bw [bird]           Scrapes birdweb.org for the bird
aab [bird]          Scrapes allaboutbirds.org for the bird

"""
if __name__ == "__main__":
    
    import sys
    import glob
    from filedb import FileDB
    from filecache import FileCache
    import config
    import pprint
    import scrapers
    import re
    import requests
    
    db = FileDB(config.DATA_DIR)
    cache = FileCache(config.CACHE_DIR)
    pp = pprint.PrettyPrinter(indent=2)
    
    # Turns a full name of a bird into the short name for
    # URLs. Maps to urls on BW and AAB.
    def short_name(long_name):
        s = long_name.lower().replace(' ', '_')
        return re.sub('[^a-z_-]', '', s)

    def cached_request(cache, url, force=False):
        if not cache.has(url) or force:
            r = requests.get(url)
            html = r.text
            cache.put(url, html)
        return cache.get(url)
    
    # Partial application for convenience
    cached_requester = lambda url: cached_request(cache, url)

    def scrape_checklist(cache, db, checklist_name):
        checklist = db.get('checklists', checklist_name)
        
        if not checklist:
            print 'Initialize the checklist in the db first'
            return
            
        url = checklist['url']
        content = cached_request(cache, url)
        res = scrapers.scrape_checklist(content)
        return res
        
    def populate_checklist(cache, db, checklist_name):
        checklist = scrape_checklist(cache, db, checklist_name)
        
        # transform frequencies to JSON API format
        checklist = [
            {
                'url_bird': '/birds/'+short_name(bird),
                'frequencies': freqs
            } for bird, freqs in checklist.items()
        ]
        
        # save the frequencies in the checklist since
        # these vary by location
        db.patch('checklists', checklist_name, {
            'items': checklist
        })
    
    # `frequency` can be multiple characters 'CFU'
    def birds_in(db, checklist_name,  month, frequency):
         months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Dec']
         frequencies = ['C', 'F', 'U', 'R', 'I']
         if month not in months:
             print 'Valid months:'
             print months
         month_index = months.index(month)
         if frequency not in frequencies:
             print 'Valid frequencies:'
             print frequencies
         
         
         checklist = db.get('checklists', checklist_name)
         print checklist.keys()
         for item in checklist['items']:
             if item['frequencies'][month_index] in frequency:
                 print item['url_bird']
    
    def birdweb(cache, bird):
        url = "http://www.birdweb.org/birdweb/bird/%s" % bird
        content = cached_request(cache, url, False)
        scraper = scrapers.BirdWebScraper(cached_requester)
        ret = scraper.scrape_species_birdweb(content)
        print ret
    
    def allaboutbirds(cache, bird):
        pass
    
    def main(cmd_args):
        import optparse
        usage = "\n%prog [options] command [input-file-pattern]\n" + cmd_doc
        oparser = optparse.OptionParser(usage)
        
        options, args = oparser.parse_args(cmd_args)
        cmd = args[0]

        if cmd == 'checklist':
            pp.pprint(db.get('checklists', args[1]))
        if cmd == 'scrape_checklist':
            scrape_checklist(cache, db, args[1])
        if cmd == 'populate_checklist':
            populate_checklist(cache, db, args[1])
        if cmd == 'birds_in':
            birds_in(db, args[1], args[2], args[3])
        if cmd == 'bw':
            birdweb(cache, args[1])
        if cmd == 'aab':
            allaboutbirds(cache, args[1])
            
    av = sys.argv[1:]
    main(av)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    