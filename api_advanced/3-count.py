#!/usr/bin/python3
"""Module that recursively counts keyword occurrences in hot articles."""
import requests


def count_words(subreddit, word_list, counts={}, after=None):
    """Recursively count and print sorted keyword occurrences."""
    url = "https://www.reddit.com/r/{}/hot.json?limit=100".format(subreddit)
    headers = {"User-Agent": "MyRedditApp/1.0"}
    params = {"after": after} if after else {}
    response = requests.get(
        url, headers=headers, params=params, allow_redirects=False)
    if response.status_code != 200:
        return
    data = response.json()
    posts = data.get("data", {}).get("children", [])
    after = data.get("data", {}).get("after")
    for post in posts:
        title = post.get("data", {}).get("title", "").lower().split()
        for word in word_list:
            w = word.lower()
            for t in title:
                if t == w:
                    counts[w] = counts.get(w, 0) + 1
    if after is None:
        sorted_counts = sorted(counts.items(), key=lambda x: (-x[1], x[0]))
        for word, count in sorted_counts:
            if count > 0:
                print("{}: {}".format(word, count))
        return
    return count_words(subreddit, word_list, counts, after)

