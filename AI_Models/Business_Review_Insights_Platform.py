import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import urllib.parse
from textblob import TextBlob
import plotly.express as px

class ReviewScraper:
    def __init__(self):
        pass

    def search_business(self, query: str) -> dict:
        """
        Enhanced search for a business using Bing Search Engine.
        """
        encoded_query = urllib.parse.quote(f"{query} reviews")
        search_url = f"https://www.bing.com/search?q={encoded_query}"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        try:
            response = requests.get(search_url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract all relevant links
            links = soup.find_all('a', href=True)
            for link in links:
                href = link['href']
                if "review" in href or "rating" in href:
                    # Ensure the URL has a scheme
                    full_url = urllib.parse.urljoin("https://www.bing.com", href)
                    return {"name": query, "url": full_url}

            return {"name": query, "url": None}
        except requests.exceptions.RequestException as e:
            st.error(f"Error searching for business: {e}")
            return None

    def scrape_reviews(self, search_result: dict) -> list:
        """
        Enhanced scraping for reviews
        """
        if not search_result or not search_result.get('url'):
            return []

        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            response = requests.get(search_result['url'], headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # Attempt to locate review elements
            review_elements = soup.find_all('p')  # Adjust tag based on website structure
            reviews = []

            for element in review_elements[:10]:  # Limit to 10 reviews
                review_text = element.get_text(strip=True)
                if len(review_text) > 30:  # Filter irrelevant/short texts
                    sentiment = self.advanced_sentiment_analysis(review_text)
                    reviews.append({
                        "text": review_text,
                        "sentiment_score": sentiment['score'],
                        "sentiment_label": sentiment['label']
                    })

            return reviews
        except requests.exceptions.RequestException as e:
            st.error(f"Error scraping reviews: {e}")
            return []

    def advanced_sentiment_analysis(self, text: str) -> dict:
        """
        Perform advanced sentiment analysis using TextBlob
        """
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity

        # Categorize sentiment
        if polarity > 0.5:
            label = "Very Positive"
        elif polarity > 0:
            label = "Positive"
        elif polarity == 0:
            label = "Neutral"
        elif polarity > -0.5:
            label = "Negative"
        else:
            label = "Very Negative"

        return {
            "score": polarity,
            "label": label
        }

def main():
    st.set_page_config(page_title="Business Review Analysis", layout="wide")
    st.title("🌐 Business Review Insights Platform")

    # Sidebar for inputs
    st.sidebar.header("🏢 Business Profile")
    business_name = st.sidebar.text_input("Business Name", placeholder="Enter business name")

    # Trigger review analysis
    if st.sidebar.button("Generate Business Report"):
        if not business_name:
            st.error("Please provide a business name")
        else:
            scraper = ReviewScraper()

            # Search for Business
            search_result = scraper.search_business(business_name)

            if search_result and search_result.get('url'):
                # Scrape Reviews
                reviews = scraper.scrape_reviews(search_result)

                # Display Results
                st.header(f"Business Insights: {search_result['name']}")

                # Review Analysis
                st.subheader("Review Analysis")
                review_df = pd.DataFrame(reviews)

                if not review_df.empty:
                    # Sentiment Distribution
                    fig_sentiment = px.pie(
                        review_df,
                        names='sentiment_label',
                        title='Review Sentiment Distribution'
                    )
                    st.plotly_chart(fig_sentiment)

                # Detailed Reviews
                st.subheader("Detailed Reviews")
                for review in reviews:
                    st.markdown(f"**Sentiment: {review['sentiment_label']}**\n- {review['text']}")
            else:
                st.error("Could not find business information. Please check the name and try again.")

if __name__ == "__main__":
    main()

# Note:
# 1. This script uses Bing Search instead of Google to fetch business links.
# 2. Web scraping results depend on the structure of the target page and may require adjustments.
# 3. Use APIs like Yelp or similar for more reliable and detailed data.
