import os
import requests
import time
from dotenv import load_dotenv

def get_NYT(name, date="Today"):
    load_dotenv()
    api_key = os.getenv("NYT_API_KEY")
    base_url = "https://api.nytimes.com/svc/search/v2/articlesearch.json"
    query = name
    headline_filter = f'headline:({name})'
    page_limit = 5  
    article_list = []
    for page in range(page_limit):
        params = {
            "q": query,
            "fq": headline_filter,
            "api-key": api_key,
            "page": page
        }
        response = requests.get(base_url, params=params)
        articles = response.json()["response"]["docs"]
        if not articles:
            break
        for article in articles:
            headline = article["headline"]["main"]
            article_list.append(headline)   
        time.sleep(12)
    
    return article_list