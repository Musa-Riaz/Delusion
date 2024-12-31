import requests
from bs4 import BeautifulSoup
import json
from selenium import webdriver




# Function to scrape Medium article details
def scrape_medium_article(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract article title
        title_tag = soup.find('meta', property='og:title')
        title = title_tag['content'] if title_tag else 'No title available'

       # Extract the full description/content
        content_div = soup.find('article')
        description = content_div.get_text(separator="\n").strip() if content_div else 'No description available'


        # Extract thumbnail URL
        thumbnail_tag = soup.find('meta', property='og:image')
        thumbnail_url = thumbnail_tag['content'] if thumbnail_tag else 'No thumbnail available'

        # Check if the page contains "member-only" indicator
        member_only = False
        if soup.find(string="member-only story") or soup.find(class_="meteredContent"):
                member_only = True

        # Extract author names
        author_tag = soup.find('meta', attrs={'name': 'author'})
        author = author_tag['content'] if author_tag else 'No author information available'

        # Extract tags
        tags = []
        tag_elements = soup.find_all('a', class_='tags')
        for tag in tag_elements:
            tags.append(tag.get_text(strip=True))

        return {
            "title": title,
            "description": description,
            "thumbnail_url": thumbnail_url,
            "member_only": member_only,
            "author": author,
            "tags": tags
        }

    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return {
            "error": "Failed to fetch the article",
            "details": str(e)
        }

# Save data to a JSON file
def save_to_json(data, filename="medium_articles.json"):
    try:
        existing_data = []
        # Load existing data if the file exists
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                existing_data = json.load(file)
        except FileNotFoundError:
            pass

        # Append new data and save
        existing_data.append(data)
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(existing_data, file, indent=4, ensure_ascii=False)
        print(f"Data successfully saved to {filename}")
    except Exception as e:
        print(f"Error saving to JSON: {e}")

# Main function
def main():
    url = input("Enter the Medium article URL: ")
    article_data = scrape_medium_article(url)
    save_to_json(article_data)

if __name__ == "__main__":
    main()
