import os
import requests
import time

def get_NYT(name, date="Today"):

    api_key = os.getenv("NYT_API_KEY")
    base_url = "https://api.nytimes.com/svc/search/v2/articlesearch.json"
    query = name
    headline_filter = f'headline:({name})'
    page_limit = 10  
    article_list = []
    for page in range(page_limit):
        params = {
            "q": query,
            "fq": headline_filter,
            "api-key": api_key,
            "page": page
        }
        response = requests.get(base_url, params=params)
        article = response.json()["response"]["docs"]["headline"]["main"]
        if not article:
            break
        article_list.append(article)
        time.sleep(12)
    
    return article_list