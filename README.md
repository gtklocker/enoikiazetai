# enoikiazetai

This is a scraper used to create a map with all the house listings in Ioannina, using data from [enoikiazetai.uoi.gr](http://enoikiazetai.uoi.gr/).

## Usage

    pip install -r requirements.txt
    python scrape.py

This will create `ads.geojson`, which can be rendered using any GeoJSON
rendering tool. [Here](https://gist.github.com/gtklocker/6b2e58f26599f5e78c98)
is an example of such a file rendered in Github.
