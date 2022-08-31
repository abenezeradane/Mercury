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
        return f"Product #{self.NUM}\n  Name: '{self.NAME}',\n  Condition: {self.COND},\n  Price: {self.PRICE}\n  URL: {self.URL}"


# Downloads a given eBay product URL
def download(URL: str) -> tuple[str, str]:
    """ Downloads the raw HTML of a given website and return it as a tuple along with the URL """

    # GET the product URL
    response = requests.get(URL, headers = {'Accept-Encoding': 'identity'})

    # Verify that the request was successful
    if not response:
        print(f"{BOLD_RED}Error: {WHITE}GET request for '{URL}' returned a status code of {response.status_code}...{RESET}")
        sys.exit()

    # Return a tuple containing the URL and HTML
    return URL, response.text


# Parses the HTML string of an eBay product for wanted components
def parse(data: tuple[str, str]) -> Product:
    """ Parses a raw HTML string and returns a 'Product' dataclass based on the components """

    # Create a Beautiful Soup instance
    soup = BeautifulSoup(data[1], "lxml")
    
    # Verify that the creation of the Beautiful Soup instance was successful
    if not soup:
        print(f"{BOLD_RED}Error: {WHITE}Unable to create Beautiful Soup instance from '{data[0]}'...{RESET}")
        sys.exit()

    # Parse the product components
    name = soup.find("h1").get_text()[1:]                                                                           # Remove the extra space infront of the item name
    number = data[0][25:37]                                                                                         # Parse specific product number from the URL
    condition = soup.find("div", {"class": "d-item-condition-text"}).find("span", {"class": "clipped"}).get_text()  # Ignore duplicate condition text
    price = soup.find("span", {"id": "prcIsum"}).get_text()                                                         # Find the specific span using its ID
    
    # Return the constructed product
    return Product(data[0], number, name, condition, price)


# Write the Product data into a file
def write(filename: str, product: Product) -> bool:
    """ Attempts to write products into a file, return true if successful """

    # Write Product data to file
    output = None

    try:
        if not exists(filename):                                                                        # If the file doesn't exist, create the file and write the header
            output = open(filename, "w+")
            output.write("ITEM_NUMBER,NAME,CONDITION,PRICE,URL\n")
        else:                                                                                           # If the file exists, open and append to the file
            output = open(filename, "a+")

        output.write(f"{product.NUM},{product.NAME},{product.COND},{product.PRICE},{product.URL}\n")    # Write the product data
        output.close()
    except Exception:
        print(f"{BOLD_RED}{Exception} Error: {WHITE}Unable to create/write to file '{filename}'...{RESET}")
        sys.exit()


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

    # Based on argument type (URL or file), parse the product(s)
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

        # Define URL, tuple, and product lists
        alpha = list()  # List to contain product URLs
        gamma = list()  # List to contain tuples (product URL and product HTML)
        omega = list()  # List to contain Products

        # Save product URLs in data file to list
        try:
            file = open(args.file, "r")
            alpha = file.readlines()
        except Exception:
            print(f"{BOLD_RED}{Exception} Error: {WHITE}Unable to parse data from file '{args.file}'...{RESET}")
            sys.exit()

        # Determine the number of processes to run
        processes = min(NUM_OF_CORES, len(alpha))

        # Parse all the product URLs
        with Pool(processes = processes) as pool:
            gamma += pool.map(download, alpha)  # Download every product HTML
            omega += pool.map(parse, gamma)     # Parse every HTML string

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