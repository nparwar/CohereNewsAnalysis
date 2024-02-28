import os
import requests
import time
from dotenv import load_dotenv
from datetime import datetime, timedelta

#function to get correct dates
def get_Date_Range(time_period):
    today = datetime.now()
    if time_period == "Today":
        begin_date = end_date = today
    elif time_period == "Past Week":
        begin_date = today - timedelta(weeks=1)
        end_date = today
    elif time_period == "Past Month":
        begin_date = today - timedelta(days=30)  # Approximating a month as 30 days
        end_date = today
    elif time_period == "Past 6 Months":
        begin_date = today - timedelta(days=6*30)  # Approximating 6 months as 180 days
        end_date = today
    elif time_period == "Past Year":
        begin_date = today - timedelta(days=365)
        end_date = today
    else:
        raise ValueError("Invalid time_period")

    # Format dates as YYYYMMDD
    begin_date_str = begin_date.strftime("%Y%m%d")
    end_date_str = end_date.strftime("%Y%m%d")

    return begin_date_str, end_date_str


def get_NYT(name, date="Today"):
    load_dotenv()
    api_key = os.getenv("NYT_API_KEY")
    base_url = "https://api.nytimes.com/svc/search/v2/articlesearch.json"
    query = name
    headline_filter = f'headline:({name})'
    page_limit = 10  
    article_list = {}
    beginDate, endDate = get_Date_Range(date)
    print(beginDate, endDate)
    for page in range(page_limit):
        params = {
            "q": query,
            "fq": headline_filter,
            "api-key": api_key,
            "page": page,
            "begin_date": beginDate,
            "end_date": endDate
        }
        response = requests.get(base_url, params=params)
        articles = response.json()["response"]["docs"]
        if not articles:
            break
        for article in articles:
            article_list[article["headline"]["main"]] = article["pub_date"] 
        time.sleep(12)
    
    return article_list