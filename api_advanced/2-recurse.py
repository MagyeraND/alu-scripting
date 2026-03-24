#!/usr/bin/python3
"""Module that recursively queries the Reddit API for hot articles."""
import requests


def recurse(subreddit, hot_list=[], after=None):
    """Recursively return a list of hot article titles for a subreddit."""
    url = "https://www.reddit.com/r/{}/hot.json?limit=100".format(subreddit)
    headers = {"User-Agent": "MyRedditApp/1.0"}
    params = {"after": after} if after else {}
    response = requests.get(
        url, headers=headers, params=params, allow_redirects=False)
    if response.status_code != 200:
        return None
    data = response.json()
    posts = data.get("data", {}).get("children", [])
    after = data.get("data", {}).get("after")
    for post in posts:
        hot_list.append(post.get("data", {}).get("title"))
    if after is None:
        return hot_list
    return recurse(subreddit, hot_list, after)

