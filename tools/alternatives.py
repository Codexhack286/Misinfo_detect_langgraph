import requests
from config import NEWS_API_KEY

NEWS_URL = "https://newsapi.org/v2/everything"

def fetch_alternatives(query: str):
    params = {
        "q": query,
        "language": "en",
        "sortBy": "relevancy",
        "pageSize": 5,
        "apiKey": NEWS_API_KEY
    }

    response = requests.get(NEWS_URL, params=params, timeout=10)
    data = response.json()

    if data.get("status") != "ok":
        return []

    return [
        {
            "title": article["title"],
            "source": article["source"]["name"],
            "url": article["url"]
        }
        for article in data.get("articles", [])
    ]
