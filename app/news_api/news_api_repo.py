import time
import requests
from app.db.mongo_db import initialize_mongo
from app.groq_api.text_analysis import get_event_details, init_groq
from app.settings.config import NEWS_API_KEY, DB_URL



BASE_URL = 'https://eventregistry.org/api/v1/'


def get_articles(page):
    url = BASE_URL + "article/getArticles"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "action": "getArticles",
        "apiKey": NEWS_API_KEY,
        "keyword": "terror attack",
        "ignoreSourceGroupUri": "paywall/paywalled_sources",
        "articlesPage": page,
        "resultType": "articles",
        "articlesSortBy": "socialScore",
        "articlesCount": 10,
        "articlesSortByAsc": 'false',
        "dataType": [
            "news",
            "pr"
        ],
        "forceMaxDataTimeWindow": 31
    }
    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            res = response.json()
            process_articles(res['articles']['results'])
        else:
            print(f"Request failed with status code {response.status_code}: {response.text}")
    except Exception as e:
        print("An error occurred:", str(e))



def process_articles(articles):
    print("Processing articles...")
    articles_list = []
    groq_client = init_groq()
    for article in articles:
        missing_details = get_event_details(article['body'], groq_client)
        article.update(missing_details)
        articles_list.append(article)
    print("Finished processing articles.")
    insert_articles(articles_list)


def insert_articles(articles):
    articles_col = initialize_mongo(DB_URL, "terror_attacks_db", "articles")
    articles_col.insert_many(articles)
    print(f"Inserted {len(articles)} articles")


if __name__ == "__main__":
    time_interval = 6
    page_number = 1
    for _ in range(3):
        get_articles(page_number)
        page_number += 1
        print(f"Waiting for {time_interval} seconds...")
        time.sleep(time_interval)
