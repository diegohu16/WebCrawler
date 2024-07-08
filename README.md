# WebCrawler

This is a Python script that crawls Hacker News (https://news.ycombinator.com/) and stores information about entries in a SQLite database named "crawler_data.db".

# Features

- Extracts data like rank, title, points, and comments.
- Categorizes entries based on title length (long_titles, short_titles).
- Stores entries along with the filter type and timestamp.
- Retrieves entries based on a chosen filter and sorts them (long entries by comments descending, short entries by points descending).

# How to use

- Install Dependencies:
  - You'll need the following Python libraries:
    - requests
    - beautifulsoup4
    - sqlite3
    - You can install them using pip install [requests] [beautifulsoup4] [sqlite3].
- Run the Script:
  - Execute the script using python crawler.py

# Notes

- The script currently crawls only the first page of Hacker News entries. You can modify it to crawl more pages.
- We could add error handling for potential exceptions during web scraping or database operations.

# Code summary

- get_entries() is the main function in witch we create the database, extract the data from the given URL and then store it to the database and finally we retrieve and print it in the console.
- We extract the URL data in extract_url_data() function using BeautifulSoup library. Then, we extract the data that we want to store from each entry with extract_entry_data() function.
- Once we have all the data that we want, we count the words that each title has with count_words() function and then we store it divided in long titles and short titles.
- After storing each entry we can retrieve them by making a request to the database and then print it in the terminal.
