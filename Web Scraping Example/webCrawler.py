# Credit to https://charlieojackson.co.uk/python/python-web-crawler.php
# List to store all the URLs
import sqlite3
# A Regular Expression or RegEx is a special sequence of characters that uses a search pattern to find a string or set of strings.
# It can detect the presence or absence of a text by matching it with a particular pattern and also can split a pattern into one or more sub-patterns.
import re  # Regular expression operations
import time
import requests  # HTTP client library
from bs4 import BeautifulSoup  # package for parsing HTML and XML documents

# Set the timer
start = time.time()

# List to store URLs
all_urls = []
# Counter for the while loop
link_counter = 0

# User provides the URL for crawling
url = input("URL to crawl: ")
if len(url) < 1:
    url = "https://charlieojackson.co.uk"
# Append the URL to the URL List
all_urls.append(url)

# connect to database
db = sqlite3.connect('site_crawl.db')
cursor = db.cursor()


def get_db_name(page_url):
    # Takes a URL and strips it to use as a table name
    # i.e. remove the https:// and .com and grap the first part
    split_url = ""
    if 'www' in page_url:
        split_url = re.findall('ht.*://www\.(.*?)\.', page_url)
        split_url = split_url[0].capitalize()
    else:
        split_url = re.findall('ht.*://(.*?)\.', page_url)
        split_url = split_url[0].capitalize()
    return split_url


#  Structure the database is to have individual tables for different domains
db_name = get_db_name(url)
# Table schema
# "ID" INTEGER - PRIMARY KEY AUTOINCREMENT
# "Title" varchar(255)
# "Description" varchar(255)
# "Number_of_links" INTEGER
# "Contents" TEXT
# "Time" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
# 'IF NOT EXISTS' clause means new domains will create a new table,
cursor.execute("CREATE TABLE IF NOT EXISTS " + db_name + "(ID INTEGER PRIMARY KEY AUTOINCREMENT,URL varchar(255),"
                                                         "Title varchar(255),Description varchar(255),Number_of_links "
                                                         "INTEGER,Contents TEXT, Time TIMESTAMP DEFAULT "
                                                         "CURRENT_TIMESTAMP)")


# Extracting page information
def extract_content(page_soup):
    # Extract required data for crawled page
    page_title = page_soup.title.string

    try:
        page_description = page_soup.find("meta", {"name": "description"})['content']
    except:
        page_description = "NULL"

    page_contents_raw = page_soup.text  # Plain text only
    page_contents = page_contents_raw.replace("\n", "")  # Remove the newlines
    return page_title, page_description, page_contents


# Find all the links with the method 'find_all('a')' passing in 'a' as a parameter.
# Loop through the links and run a couple conditionals
def extract_links(page_soup):
    # Extract links and link counts from page
    page_links_raw = soup.find_all('a')
    for link in page_links_raw:
        # Look for the valid URLs with same domain and append it to the list if it is not there yet.
        if str(link.get('href')).startswith(url) == True and link.get('href') not in all_urls:
            # Skip if it is jpg and png images link
            if '.jpg' in link.get('href') or '.png' in link.get('href'):
                continue
            else:
                # Append the link to our list
                all_urls.append(link.get('href'))
    # total number of links found on the page.
    total_count = len(page_links_raw)
    return total_count


# Inserting data into SQLite database
def insert_data(extracted_data):
    page_url, page_title, page_description, page_contents, page_total_links = extracted_data
    cursor.execute(
        "INSERT INTO " + db_name + " (URL, Title, Description, Number_of_links, Contents) VALUES(?,?,?,?,?)",
        (page_url, page_title, page_description, page_total_links, page_contents))
    db.commit()


# This loop runs until the counter is bigger than the length of the list i.e. there are no more URL's to crawl.
while link_counter < len(all_urls):

    try:
        print("Loop Counter: %d - Crawling: %s " % (link_counter, all_urls[link_counter]))
        r = requests.get(all_urls[link_counter])
        if r.status_code == 200:
            html = r.text
            soup = BeautifulSoup(html, "html.parser")
            # View page source
            #print(soup.prettify())
            # Getting total links count
            no_of_links = extract_links(soup)
            # Getting title, description, page contents
            title, description, contents = extract_content(soup)
            print("Page title: %s \n"
                  "Page description: %s \n"
                  "Page contents: %s \n"
                  "Total links count: %d \n" % (title, description, contents, no_of_links))
            # Insert the crawled data into the database
            insert_data((all_urls[link_counter], title, description, contents, no_of_links))
        link_counter += 1  # increment to stop the while loop

    except Exception as err:  # Error handling
        link_counter += 1  # increment to stop the while loop
        print(str(err))

# Close the table and database
cursor.close()
db.close()
# Find the total crawling time
end = time.time()
print("Total crawling time: ", end - start)
