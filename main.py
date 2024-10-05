import os
from dotenv import load_dotenv
import pandas as pd
from newsapi import NewsApiClient
from datetime import datetime, timedelta
import streamlit as st

# Load environment variables from .env
load_dotenv()
news_api_key = os.getenv("NEWS_API_KEY")  # Load News API key

# Function to fetch news articles
def fetch_news(query, from_date, to_date, language='en', sort_by='relevancy', page_size=30):
    newsapi = NewsApiClient(api_key=news_api_key)  # Use the News API key

    all_articles = newsapi.get_everything(
        q=query,
        from_param=from_date,
        to=to_date,
        language=language,
        sort_by=sort_by,
        page_size=page_size
    )

    articles = all_articles.get('articles', [])
    
    # Convert to DataFrame
    if articles:
        df = pd.DataFrame(articles)
        return df
    else:
        return pd.DataFrame()  # Return an empty DataFrame if no articles are found

# Streamlit UI
st.title("Financial News Analysis Tool")

# Input for news query
query = st.text_input("Enter the company or topic:", "Microsoft News June 2024")

# Get the current time
current_time = datetime.now()
# Get the time 10 days ago
time_10_days_ago = current_time - timedelta(days=10)

# Fetch news
df = fetch_news(query, time_10_days_ago, current_time)

# Drop 'source' column if the DataFrame is not empty
if not df.empty:
    df_news = df.drop("source", axis=1)

    # Preprocess news data
    def preprocess_news_data(df):
        df['publishedAt'] = pd.to_datetime(df['publishedAt'])
        df = df[~df['author'].isna()]  # Remove articles without an author
        df = df[['author', 'title', 'description']]  # Keep relevant columns
        return df

    preprocessed_news_df = preprocess_news_data(df_news)

    # Display the extracted news articles
    st.write("### Extracted News Articles:")
    for index, row in preprocessed_news_df.iterrows():
        st.write(f"**Author:** {row['author']}")
        st.write(f"**Title:** {row['title']}")
        st.write(f"**Description:** {row['description']}\n")

else:
    st.write("No articles found for the given query.")
