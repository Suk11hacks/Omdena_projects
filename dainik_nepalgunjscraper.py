#scraping data from dainink nepalgunj 
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Function to get article content
def get_article(url):
    article_class = "news-single-content"  # Update: class of article content
    date_class = "news-date"  # Update: class of date
    author_class = "author-name"  # Update: class of author
    location_class = "news-location"  # Update: class of location

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        article_body = soup.find("div", class_=article_class).text.strip()
        article_date = soup.find("span", class_=date_class).text.strip()
        article_author = soup.find("div", class_=author_class).text.strip()
        article_location = soup.find("div", class_=location_class).text.strip()

        article_content = [article_body, article_date, article_author, article_location]
        return article_content
    except Exception as e:
        return None


data = []
start_time = time.time()

for i in range(1, 100):
    print(f"Current loop {i}")
    url = f"https://www.dainiknepalgunj.com/page/{i}"
    print("Requesting URL:", url)  # Debugging line

    try:
        # Making a request for parsing the website
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all articles on the page
        articles = soup.find_all("div", class_="news-item")

        # Loop to get elements from the current page
        for article in articles:
            try:
                # ... (rest of the code)
                print("Article title:", article_title)  # Debugging line
                print("Full article URL:", full_article_url)  # Debugging line

                # ... (rest of the code)
            except Exception as e:
                print(f"Error occurred while processing article: {e}")
                # ... (rest of the code)
    except Exception as e:
        print(f"Error occurred while processing page: {e}")


# Data list
data = []
start_time = time.time()

for i in range(1, 100):
    print(f"Current loop {i}")
    url = f"https://www.dainiknepalgunj.com/page/{i}"

    try:
        # Making a request for parsing the website
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all articles on the page
        articles = soup.find_all("div", class_="news-item")
        
        # Loop to get elements from the current page
        for article in articles:
            try:
                article_title = article.find("h2").text.strip()  # Update: title tag
                article_url = article.find("a")["href"]  # Update: article content link
                
                full_article_url = f"https://www.dainiknepalgunj.com{article_url}"  # Update: full article content link
                article_content = get_article(full_article_url)  # Call function to get article content, date, author, location

                # Append data to the list
                data.append([article_title, *article_content])  # List to append articles
            except Exception as e:
                print(f"Error occurred while processing article: {e}")
                data.append([article_title, None, None, None, None])  # If there's an error, add None values for article content, date, author, and location
    except Exception as e:
        print(f"Error occurred while processing page: {e}")

# Create a DataFrame from the collected data
df = pd.DataFrame(data, columns=["Article Title", "Article Content", "Date", "Author", "Location"])
print(df)

# Save the DataFrame to a CSV file
df.to_csv('dainik_nepalgunj_data.csv', encoding='utf-8', index=False)

total_time = time.time() - start_time
print(f"Scraping completed in {total_time:.2f} seconds.")

