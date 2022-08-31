## Mercury

A fast and efficient eBay webscraper implemented using Beautiful Soup 

### Installation
```bash
# Clone the repo
$ git clone https://github.com/PB020/Mercury.git

# Change the working directory
$ cd mercury

# Create virtual enviroment
$ python -m venv .env
$ .env/Scripts/activate # Windows
$ .env/bin/activate # Linux/MacOS

# Install requirements
$ pip install -U -r requirements.txt
```

### Usage
```bash
usage: mercury.py [-h] [--url URL] [--file FILE] [--output OUTPUT]

A fast and efficient eBay product webscraper

optional arguments:
  -h, --help       show this help message and exit
  --url URL        URL of an eBay product ('https://www.ebay.com/itm/...')
  --file FILE      Path to a file containing ONLY eBay product URLs
  --output OUTPUT  CSV filename where parsed data should be saved
```

**Note:** If no URL or file is provided, the script will terminate.

### Example
```bash
# Single URL
$ mercury.py --url "https://www.ebay.com/itm/..."

# File containing URLs
$ mercury.py --file "input.txt"

# Output to CSV
$ mercury.py --url "https://www.ebay.com/itm/..." --output "output.csv"
```

### Output
```csv
ITEM_NUMBER,NAME,CONDITION,PRICE,URL
...,...,...,...,...
```

### Dependencies
Web Scraping:
* [lxml](https://pypi.org/project/lxml/)
* [requests](https://pypi.org/project/requests/)
* [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/)

CLI:
* [argparse](https://pypi.org/project/argparse/)
* [colorama](https://pypi.org/project/colorama/)

Multiprocessing:
* [multiprocessing](https://pypi.org/project/multiprocessing/)
### License
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)