from bs4 import BeautifulSoup
import requests
import re

# most of this function was written with the help of ChatGPT
# due to HTML structures being tedious to understand
def scrape_medium_article(url):
    try:
        # send http request
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        # for parsing html
        soup = BeautifulSoup(response.text, 'html.parser')

        title_tag = soup.find('meta', property='og:title')
        title = title_tag['content'] if title_tag else ''

        content_div = soup.find('article')
        text = content_div.get_text(separator="\n").strip() if content_div else ''

        # thumbnail is first image
        thumbnail_tag = soup.find('meta', property='og:image')
        thumbnail_url = thumbnail_tag['content'] if thumbnail_tag else 'No thumbnail available'

        # check whether the page is for members only or not
        members_only = False
        if soup.find(string="member-only story") or soup.find(class_="meteredContent"):
            members_only = True

        author_tag = soup.find('meta', attrs={'name': 'author'})
        authors = author_tag['content'] if author_tag else '[]'

        # tags are placed difficultly in the html
        # the following only returns tags for some articles
        tags = []
        tag_containers = soup.find_all('a', href=lambda href: href and "/tag/" in href)
        for tag in tag_containers:
            tags.append(tag.get_text(strip=True))

        timestamp = ''
        time_tag = soup.find('meta', property='article:published_time')
        if time_tag:
            timestamp = time_tag['content']
        else:
            # in case not found, secondary option
            time_element = soup.find('time')
            if time_element:
                timestamp = time_element.get('datetime', '')
        timestamp = re.sub(r'[A-Za-z]', ' ', timestamp)

        return {
            "title": title,
            "text": text,
            "url": url,
            "thumbnail_url": thumbnail_url,
            "members_only": 'Yes' if members_only else 'No',
            "authors": str([authors]),
            "tags": str(tags),
            "timestamp": timestamp.strip()
        }

    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        status_code = e.response.status_code if e.response else 408
        return {
            "error": "Failed to fetch the article",
            "details": str(e),
            "response_code": status_code
        }
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        status_code = e.response.status_code if e.response else 408
        return {
            "error": "An unexpected error occurred",
            "details": str(e),
            "response_code": status_code
        }