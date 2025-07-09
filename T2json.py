import os
import json
from bs4 import BeautifulSoup

def process_html_files(html_dir, json_dir):
    """Reads all HTML files in a directory, extracts tweets, and saves them as JSON files."""
    os.makedirs(json_dir, exist_ok=True)  # Ensure JSON directory exists

    # Get all HTML files in the directory
    html_files = [f for f in os.listdir(html_dir) if f.startswith("data") and f.endswith(".html")]
    
    for html_file in html_files:
        file_path = os.path.join(html_dir, html_file)
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                html_content = file.read()
            save_tweets_as_json(html_content, html_file, json_dir)
        except Exception as e:
            print(f"Error reading {html_file}: {e}")

def save_tweets_as_json(html_content, html_file, json_dir):
    """Extracts tweets from HTML and saves them in a JSON file."""
    soup = BeautifulSoup(html_content, "html.parser")
    
    tweets = []
    tweet_divs = soup.find_all("div", attrs={"data-testid": "cellInnerDiv"})  # Get full tweets

    for i, tweet_div in enumerate(tweet_divs):
        try:
            # Get username
            username_tag = tweet_div.find("div", attrs={"data-testid": "User-Name"})
            username = username_tag.get_text(strip=True) if username_tag else "Unknown"

            # Get tweet text
            tweet_text_tag = tweet_div.find("div", attrs={"data-testid": "tweetText"})
            tweet_text = " ".join(span.get_text(strip=True) for span in tweet_text_tag.find_all("span")) if tweet_text_tag else ""


            # Get all URLs in the tweet
            urls = list(set(a["href"] for a in tweet_div.find_all("a", href=True)))


            # Create tweet data dictionary
            tweet_data = {
                "id": i + 1,
                "username": username,
                "text": tweet_text,
                "urls": urls
            }
            tweets.append(tweet_data)

        except Exception as e:
            print(f"Error processing tweet {i+1} in {html_file}: {e}")

    # Save tweets from this file in a single JSON file
    json_filename = os.path.splitext(html_file)[0] + ".json"
    json_path = os.path.join(json_dir, json_filename)
    
    with open(json_path, "w", encoding="utf-8") as json_file:
        json.dump(tweets, json_file, indent=4, ensure_ascii=False)

    print(f"Saved {len(tweets)} tweets from {html_file} to {json_filename}")

# Example usage
html_dir = "HtmlFile"
json_dir = "JSONfiles"
process_html_files(html_dir, json_dir)
