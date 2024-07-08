import datetime
import re
import requests
import sqlite3
from bs4 import BeautifulSoup


def count_words(title):
    # Count the number of words of the title
    pattern = r"[^\w ]"

    replaced_title = re.sub(pattern, "", title)

    return len(replaced_title.split())


def create_db():
    # Create table to store the data
    conn = sqlite3.connect("crawler_data.db")
    cursor = conn.cursor()

    cursor.execute(
        """
            CREATE TABLE IF NOT EXISTS entries (
            rank TEXT PRIMARY KEY,
            title TEXT,
            points INTEGER,
            comments INTEGER,
            filter_type TEXT,
            timestamp TEXT
            )
        """
    )

    conn.commit()
    conn.close()


def drop_db():
    # Teardown to drop the table
    conn = sqlite3.connect("crawler_data.db")
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS entries")

    conn.commit()
    conn.close()


def extract_entry_data(data, title):
    """Extracts the data necessary of each entry"""
    entry = {}

    entry["comments"] = data.find_all("a")[3].text.split()[0]

    if entry["comments"] == "discuss":
        entry["comments"] = 0

    entry["points"] = data.find("span", class_="score").text.split()[0]
    entry["rank"] = title.find("span", class_="rank").text.strip()
    entry["title"] = title.find("span", class_="titleline").find("a").text.strip()

    return entry


def extract_url_data(url):
    """Gets the html content of the given url"""
    response = requests.get(url)
    html_content = BeautifulSoup(response.content, "html.parser")

    entries_data = html_content.find_all("span", class_="subline")
    entries_title = html_content.find_all("tr", class_="athing")

    for i in range(0, 29):
        entry_data = extract_entry_data(entries_data[i], entries_title[i])
        if count_words(entry_data["title"]) > 5:
            store_entry(entry_data, "long_titles")
        else:
            store_entry(entry_data, "short_titles")


def store_entry(entry, filter_type):
    # Stores entry data along with filter type and timestamp
    timestamp = datetime.datetime.now().isoformat()

    conn = sqlite3.connect("crawler_data.db")
    cursor = conn.cursor()

    cursor.execute(
        """INSERT INTO entries (rank, title, points, comments, filter_type, timestamp)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (
            entry["rank"],
            entry["title"],
            entry["points"],
            entry["comments"],
            filter_type,
            timestamp,
        ),
    )

    conn.commit()
    conn.close()


def get_entries():
    # Retrieves entries based on the applied filter
    create_db()

    extract_url_data("https://news.ycombinator.com/")

    conn = sqlite3.connect("crawler_data.db")
    cursor = conn.cursor()

    cursor.execute(
        """SELECT * FROM entries WHERE filter_type = 'long_titles' ORDER BY comments DESC"""
    )
    long_title_entries = cursor.fetchall()

    cursor.execute(
        """SELECT * FROM entries WHERE filter_type = 'short_titles' ORDER BY points DESC"""
    )
    short_title_entries = cursor.fetchall()

    conn.close()

    print("LONG TITLE ENTRIES:")
    for entry in long_title_entries:
        print(
            f"{entry[0]} Rank. Title: {entry[1]} ({entry[2]} points, {entry[3]} comments)"
        )

    print("SHORT TITLE ENTRIES:")
    for entry in short_title_entries:
        print(
            f"{entry[0]} Rank. Title: {entry[1]} ({entry[2]} points, {entry[3]} comments)"
        )

    drop_db()


get_entries()
