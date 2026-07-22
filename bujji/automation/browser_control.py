"""
Browser Control — Web Browser Automation & Searches
====================================================
Web browsing, Google search, YouTube search, Wikipedia, and RSS news fetching.
"""

import webbrowser
import urllib.parse
import requests
from bs4 import BeautifulSoup


def open_url(url):
    """Open URL in default web browser."""
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    webbrowser.open(url)
    return f"Opening {url}"


def google_search(query):
    """Perform Google Search in browser."""
    clean_q = query.replace("search google for", "").replace("google", "").strip()
    encoded = urllib.parse.quote(clean_q)
    url = f"https://www.google.com/search?q={encoded}"
    webbrowser.open(url)
    return f"Searching Google for '{clean_q}'"


def youtube_search(query):
    """Perform YouTube Search in browser."""
    clean_q = query.replace("search youtube for", "").replace("youtube", "").strip()
    encoded = urllib.parse.quote(clean_q)
    url = f"https://www.youtube.com/results?search_query={encoded}"
    webbrowser.open(url)
    return f"Searching YouTube for '{clean_q}'"


def fetch_news_rss(category="technology"):
    """Fetch top news headlines via Google News RSS."""
    try:
        url = "https://news.google.com/rss"
        if category and category.lower() != "top":
            url = f"https://news.google.com/rss/search?q={urllib.parse.quote(category)}"

        resp = requests.get(url, timeout=5)
        resp.raise_for_status()

        try:
            soup = BeautifulSoup(resp.content, "xml")
        except Exception:
            soup = BeautifulSoup(resp.content, "html.parser")

        items = soup.find_all("item", limit=10)

        articles = []
        for item in items:
            articles.append({
                "title": item.title.text if item.title else "No Title",
                "link": item.link.text if item.link else "#",
                "pub_date": item.pubDate.text if item.pubDate else "",
            })
        return articles
    except Exception as e:
        print(f"[News RSS Error] {e}")
        return []
