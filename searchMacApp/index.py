# 用必应搜索“pixelmator pro”，从搜索的结果中找标题有“Mac App Store 上的”
import requests
from bs4 import BeautifulSoup

# Send a GET request to Bing with the search query
response = requests.get("https://www.bing.com/search?q=pixelmator+pro")

# Parse the HTML content of the response with BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find all the search result titles that contain "Mac App Store 上的"
titles = soup.find_all('h2', class_='b_searchboxTitle')
mac_app_store_titles = [title for title in titles if "Mac App Store 上的" in title.text]

# Print the titles that contain "Mac App Store 上的"
for title in mac_app_store_titles:
    print(title.text)
