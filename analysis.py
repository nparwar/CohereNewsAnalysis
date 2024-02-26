import streamlit as st
import os
import requests
import time
from retrieve import get_NYT

#Get NYT Articles
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


def main():
    #UI
    st.title("Company Sentiment Analysis News Aggregator")

    company_name = st.text_input("Enter a company name: ")
    
    #TimeFrame Selector
    date = st.radio(
        "Select your timeframe:",
        ["Today", "Past Week", "Past Month", "Past 6 Months", "Past Year"],
        index=0,
    )

    st.write("You selected:", date)

    search_button = st.button("Search")
    
    #Start Analysis
    if search_button and company_name:
        articles = get_news_articles(company_name)
        st.write(articles)



if __name__ == "__main__":
    main()