import requests
from bs4 import BeautifulSoup


def extract_entry_data(data, title):
    """Extracts the data necessary of each entry"""
    entry = {}

    entry["comments"] = data.find_all("a")[3].text.split()[0]
    entry["points"] = data.find("span", class_="score").text.split()[0]
    entry["rank"] = title.find("span", class_="rank").text.strip()
    entry["title"] = title.find("span", class_="titleline").find("a").text.strip()

    return entry


def get_data(url):
    """Gets the html content of the given url"""
    response = requests.get(url)
    html_content = BeautifulSoup(response.content, "html.parser")

    entries_data = html_content.find_all("span", class_="subline")
    entries_title = html_content.find_all("tr", class_="athing")

    for i in range(0, 29):
        entry_data = extract_entry_data(entries_data[i], entries_title[i])


get_data("https://news.ycombinator.com/")
