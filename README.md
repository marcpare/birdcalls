birds
===

Next up
---

- Set up /family/new API call
- Refactor scraper to have pluggable output for scraping output
--> one of output targets is HTTP REST API
--> one of output targets is stdout
- Send families to REST api



- sql data model
-- generate CSV to import bird data from JSON? from Cached?


(1) More calls for each bird
(2) Flip through pics for each bird
(3) Easily change date range for birds
(4) Yoga Mode using Chrome speech API : http://updates.html5rocks.com/2014/01/Web-apps-that-talk---Introduction-to-the-Speech-Synthesis-API
(5) iFrame with Cornell info (_or_ scrape it and render it more nicely for mobile)

Another way to viz the main menu?
Another way to cluster the collections?

- scroll down and reveal the Cornell page?
- scrape more calls
- link to Cornell bird pages?
- style? location? moving dates?
- more calls for each bird

TODO
---

* fabric may have a vagrant tools package instead of the ad-hoc method used
* mysql install pops up a bunch of dialogs


Scraper Design
---

Would be much easier if the scraper could access the database. (Can query, then scrape based on query results)

(1) Bootstrap the db
(2) Subsequent scraper functions depend on the db

Access database over JSON API with nice Python bindings


Setting up app
---

sudo pip install virtualenv
cd app
virtualenv env
. env/bin/activate

fab vagrant bootstrap

Installing fabric
---

export CFLAGS=-Qunused-arguments export CPPFLAGS=-Qunused-arguments
pip install fabric