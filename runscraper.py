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
         
         return [item for item in checklist['items']
             if item['frequencies'][month_index] in frequency]         
    
    def birdweb(bird):
        scraper = scrapers.BirdWebScraper(cached_requester)
        return scraper.species(bird)
    
    def allaboutbirds(bird):
        scraper = scrapers.AllAboutBirdsScraper(cached_requester)
        return scraper.species(bird)
        
    def detail_checklist(db, checklist_name):
        checklist = db.get('checklists', checklist_name)
        for item in checklist['items']:
            url_bird = item['url_bird']
            bird_name = url_bird.split('/')[-1]
            bird = db.get('birds', bird_name)
            
            print bird_name
            
            try:
                a = birdweb(bird_name)
                bird.update(a)
            except:
                print 'FAILED BW' + bird_name
                
            try:
                b = allaboutbirds(bird_name)
                bird.update(b)
            except:
                print 'FAILED AAB' + bird_name
            
            db.post('birds', bird_name, bird)
    
    # Clusters by Habitat for a given month and frequencies
    def cluster_checklist(db, checklist_name, month, frequency):        
        items = birds_in(db, checklist_name, month, frequency)
        
        clusters = {}
        for item in items:
            bird_name = item['url_bird'].split('/')[-1]
            bird = db.get('birds', bird_name)
            if 'habitat' in bird:
                h = bird['habitat']
                print "%s lives in %s" % (bird_name, h)
                cluster = clusters.get(h, [])
                cluster.append(bird) # plop the whole entity for now
                cluster.append(item['url_bird'])
                clusters[h] = cluster
        
        clusters = [
            {
                'name': name,
                'birds': birds
            } for (name, birds) in clusters.items()
        ]
        
        db.post('habitat_clusters', checklist_name, clusters)
    
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
            pp.pprint(birds_in(db, args[1], args[2], args[3]))
        if cmd == 'bw':
            pp.pprint(birdweb(cache, args[1]))
        if cmd == 'aab':
            pp.pprint(allaboutbirds(args[1]))
        if cmd == 'detail_checklist':
            detail_checklist(db, args[1])
        if cmd == 'cluster_checklist':
            cluster_checklist(db, args[1], args[2], args[3])
        
    av = sys.argv[1:]
    main(av)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    