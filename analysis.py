import streamlit as st
from retrieve import get_NYT


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
        articles = get_NYT(company_name)
        st.write(articles)



if __name__ == "__main__":
    main()