# velogames-schedule
Scrape data and create a simple page to view the schedule of riders in the Velogames Sprint Classics

This is a collection of scripts that gather data from Velogames and
ProCyclingStats - just a few pages, not a full-fledged network hog spider -
and merges into a webpage to facilitate making the decision of when to change
riders.

To download and process the data it uses:

* [Requests](http://docs.python-requests.org/en/master/) to keep my sanity downloading pages.
* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) to parse the pages.
* [pytz](https://pypi.python.org/pypi/pytz) to get time of update (maybe overkill too).

On the front end:

* [DataTables](https://datatables.net) to present the data.

Also a couple of [Jupyter](https://jupyter.org/) notebooks were used to start tinkering with the data.

TODO:

* ~~Improve merging speed (Not the best approach doing full boolean indexing inside an apply function).~~
* ~~Generate a json instead of a csv so we can load the data into JS directly.~~
