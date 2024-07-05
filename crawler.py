import requests
from bs4 import BeautifulSoup


def get_data(url):
    """Gets the html content of the given url"""
    response = requests.get(url)
    html_content = BeautifulSoup(response.content, "html.parser")


get_data("https://news.ycombinator.com/")
