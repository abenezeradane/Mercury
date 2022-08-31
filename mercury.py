# Import CLI Utility  Libraries
import argparse
from colorama import init

# Import Web Scraping Libraries
import lxml
import requests
from bs4 import BeautifulSoup

# Import Utility Libraries
from enum import Enum
from multiprocessing import Pool
from dataclasses import dataclass

# Define Global ANSI Escape Codes
UP = "\x1b[1A"      # Moves the cursor up one line
ERASE = "\x1b[2K"   # Erases the the line the cursor is on


# Defines the "Product" dataclass
@dataclass
class Product:
    URL: str
    NAME: str
    COND: str
    PRICE: str


# Download a given URL
def download(URL: str) -> tuple:
    """ Downloads the raw HTML of a given website and return it as a tuple along with the URL """

    pass


# Parses a given HTML string for wanted components
def parse(HTML: str) -> Product:
    """ Parses a raw HTML string and returns a 'Product' dataclass based on the components """

    pass


# Main method of application
def main() -> None:
    """ Reads command line arguments, parses the data then calls the appropriate function """
    
    pass


if __name__ == "__main__":
    init()  # Initialize Colorama
    main()  # Call the main method