import argparse
import re
import requests
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs

parser = argparse.ArgumentParser()
parser.add_argument("--file", help="html file to read comments from", required=True)
parser.add_argument("--api_token", help="YouTube API Token", required=True)
args = parser.parse_args()

private_videos = 0
invalid_urls = 0

with open(Path(args.file), "r") as file:
    soup = BeautifulSoup(file.read(), 'html.parser')
    print(soup.title)
    commented_on_list = soup.find_all(text=re.compile('Commented on'))
    comment_wrappers = [commented_on.parent for commented_on in commented_on_list]

    for comment_wrapper in comment_wrappers:
        if comment_wrapper.name == "div":
            if link := comment_wrapper.find("a", href=True):
                href = link['href']
                query = str(urlparse(href).query)
                if comment_id := parse_qs(query).get("lc"):
                    response = requests.get(f"https://www.googleapis.com/youtube/v3/comments?part=snippet&id={comment_id}&textFormat=html&key={args.api_token}")
                    response.json()
                else:
                    print("Invalid URL")
                    invalid_urls += 1
            else:
                print("Private Video")
                private_videos += 1
