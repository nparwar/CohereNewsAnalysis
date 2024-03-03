import streamlit as st
from retrieve import get_NYT
import pandas as pd
from classify import classify_Data
import matplotlib.pyplot as plt
import pandas_datareader as pdr

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
        articles = get_NYT(company_name, date)
        articles_list = [{'Title': title, 'Date': date} for title, date in articles.items()]
        df = pd.DataFrame(articles_list, columns=["Title", "Date"])
        print(df)
        if(df.empty):
            st.write("No Articles Found. Try extending the time period or picking another company.")
        else:
            df_final = classify_Data(df)
            df_final['Date'] = pd.to_datetime(df_final['Date']).dt.date
            df_final = df_final.sort_values(by='Date')
            st.write(df_final)
            # Map sentiments to scores
            sentiment_scores = {'positive': 1, 'neutral': 0, 'negative': -1}
            df_final['Score'] = df_final['Sentiment'].map(sentiment_scores)
            # Plotting
            # Calculate the cumulative sum
            grouped_df = df_final.groupby('Date').sum()
            grouped_df['Cumulative_Sum'] = grouped_df['Score'].cumsum()
            plt.figure(figsize=(10, 5))
            plt.plot(grouped_df.index, grouped_df["Cumulative_Sum"], marker='o')
            plt.xlabel('Date')
            plt.ylabel('Cumulative Score')
            plt.title('Cumulative Sentiment Score Over Time')
            plt.grid(True)
            print(grouped_df)
            # Display the plot in Streamlit
            st.pyplot(plt)



if __name__ == "__main__":
    main()