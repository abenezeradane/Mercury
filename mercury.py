# Import CLI Utility  Libraries
import argparse
from colorama import init

# Import Web Scraping Libraries
import lxml
import requests
from bs4 import BeautifulSoup

# Import Utility Libraries
import sys
from os.path import exists
from multiprocessing import Pool
from dataclasses import dataclass

# IMPORTANT: Define your CPU's number of cores
NUM_OF_CORES = 8

# Define ANSI Escape Codes
UP = "\x1B[1A"              # Moves the cursor up one line
ERASE = "\x1B[2K"           # Erases the the line the cursor is on

BOLD_RED = "\x1B[1;31m"     # Changes the text style to bold and the color to red
BOLD_BLUE = "\x1B[1;34m"    # Changes the text style to bold and the color to blue
BOLD_GREEN = "\x1B[1;32m"   # Changes the text style to bold and the color to green

BLINK_RED = "\x1B[5;31m"    # Changes the text style to blinking and the color to red
BLINK_GREEN = "\x1B[5;32m"  # Changes the text style to blinking and the color to green

WHITE = "\x1B[37m"          # Changes the text style to bold and the color to white
RESET = "\x1B[0m"           # Resets all text styles and color


# Defines the "Product" dataclass
@dataclass
class Product:
    URL: str    # Product URL
    NUM: int    # Product number
    NAME: str   # Product name
    COND: str   # Product condition
    PRICE: str  # Product price

# Formatted representation of Product
def __str__(self):
    """ Returns a formated string containing the product's components """
    return f"Product {self.NUM}\n\tName: {self.NAME},\n\tCondition: {self.COND},\n\tPrice: {self.PRICE}\n\tURL: {self.URL}"


# Downloads a given eBay product URL
def download(URL: str) -> tuple[str, str]:
    """ Downloads the raw HTML of a given website and return it as a tuple along with the URL """

    return URL, URL


# Parses the HTML string of an eBay product for wanted components
def parse(product: tuple[str, str]) -> Product:
    """ Parses a raw HTML string and returns a 'Product' dataclass based on the components """

    pass


# Write the Product data into a file
def write(filename: str, product: Product) -> bool:
    """ Attempts to write products into a file, return true if successful """

    pass


# Main method of application
def main() -> None:
    """ Reads command line arguments, parses the data then calls the appropriate functions """

    # Initialize the argument parser
    parser = argparse.ArgumentParser(description = "A fast and efficient eBay product webscraper")
    parser.add_argument("--url", action = "store", help = "URL of an eBay product ('https://www.ebay.com/itm/...')")
    parser.add_argument("--file", action = "store", help = "Path to a file containing ONLY eBay product URLs")
    parser.add_argument("--output", action = "store", help = "CSV filename where parsed data should be saved")
    args = parser.parse_args()

    # Verify that command line arguments were passed
    if (args.url == None) and (args.file == None):
        print(f"{BOLD_RED}Error: {WHITE}Neither a URL nor a filename was provided...{RESET}")
        sys.exit()

    # Verify that only one command line arguments was passed
    if (args.url != None) and (args.file != None):
        print(f"{BOLD_RED}Error: {WHITE}Both a URL and a filename were provided...{RESET}")
        sys.exit()

    # Based on argument type (url or file), parse the product(s)
    if args.url != None:
        # Verify that URL is an eBay product
        if "https://www.ebay.com/itm/" not in args.url:
            print(f"{BOLD_RED}Error: {WHITE}URL '{args.url}' is not a valid eBay product...{RESET}")
            sys.exit()

        # Download the product HTML
        data = download(args.url)

        # Parse the HTML for components
        product = parse(data)

        # Write output to file if prompted
        if (args.output != None) and (".csv" in args.output[-4:]):
            write(args.output, product)

        # Print parsed data
        print(product)
    else:
        # Verify that the file containing the product URLs exists
        if not exists(args.file):
            print(f"{BOLD_RED}Error: {WHITE}File '{args.file}' does not exist...{RESET}")
            sys.exit()

        # Define url, tuple, and product lists
        alpha = list()  # List to contain product URLs
        gamma = list()  # List to contain tuples (product url and product HTML)
        omega = list()  # List to contain Products

        # Save product URLs in data file to list
        try:
            file = open(args.file, "r")
            alpha = file.readlines()
        except Exception as exception:
            print(f"{BOLD_RED}{exception} Error: {WHITE}Unable to parse data from file '{args.file}'...{RESET}")
            sys.exit()

        # Determine the number of processes to run
        processes = min(NUM_OF_CORES, len(alpha))

        # Parse all the product URLs
        with Pool(processes = processes) as pool:
            # Download every product HTML
            gamma += pool.map(download, alpha)

            # Parse every HTML string
            omega += pool.map(parse, gamma)

        # Write output to file if prompted
        if (args.output != None) and (".csv" in args.output[-4:]):
            for product in omega:
                write(args.output, product)

        # Print parsed data
        for product in omega:
            print(product)


if __name__ == "__main__":
    init()  # Initialize Colorama
    main()  # Call the main method