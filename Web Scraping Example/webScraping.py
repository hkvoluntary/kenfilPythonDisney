
from bs4 import BeautifulSoup
html_doc = """
<html><head><title>Hello World</title></head> <body><h2>Test Header</h2>
<p>This is a test.</p>
<a id="link1" href="https://my_link1">Link 1</a>
<a id="link2" href="https://my_link2">Link 2</a> 
<p>Hello, <b class="boldtext">Bold Text</b></p> </body></html>
"""
# Use Beautiful Soup decode HTML
soup = BeautifulSoup(html_doc, 'html.parser')
print(soup.prettify())

# Get title tag
title_tag = soup.title
print(title_tag)

# Get <title>...</title> String
print(title_tag.string)

# Get All link tags and url
a_tags = soup.find_all('a')
for tag in a_tags:
    print(tag.string)
    print(tag.get('href'))

tags = soup.find_all(["a", "b"])
print(tags) # return as list


## Real Example
import requests
# URL of the page to scrape
url = 'http://quotes.toscrape.com/page/1/'

# Send a GET request to the page
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the page content
    soup = BeautifulSoup(response.text, 'html.parser')

    print(soup.prettify())
    # Find all quote containers
    quotes = soup.find_all('div', class_='quote')

    for quote in quotes:
        # Extract the quote text
        text = quote.find('span', class_='text').text.strip()

        # Extract the author
        author = quote.find('small', class_='author').text.strip()

        # Extract the tags
        tags = [tag.text.strip() for tag in quote.find_all('a', class_='tag')]

        print(f"Quote: {text}")
        print(f"Author: {author}")
        print(f"Tags: {', '.join(tags)}")
        print('-' * 40)

else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")




