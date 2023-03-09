import requests
from pathlib import Path
import json
import time
import random

if Path('cache.json').is_file():
    seen_urls = json.load(open('cache.json'))
else:
    seen_urls = []


while True:
    print(seen_urls)
    page_text = requests.get('https://comicskingdom.com/rae-the-doe').text
    # maybe switch to `<link rel="canonical" href="https://comicskingdom.com/rae-the-doe/2023-03-08" />` instead of `<meta property="og:url" content='https://comicskingdom.com/rae-the-doe/2023-03-08' />`
    target_tag = [line for line in page_text.splitlines() if line.startswith('<meta property="og:url"')][0]
    comic_url = target_tag[target_tag.find("'") + 1: target_tag.rfind("'")]
    if comic_url not in seen_urls:
        seen_urls.insert(0, comic_url)
        json.dump(seen_urls, open('cache.json', 'w'))

    items = []
    for url in seen_urls[:10]:
        items.append(f'''
         <item>
      <title>Rae the Doe {url[-10:]}</title>
      <description>Here is some text containing an interesting description.</description>
      <link>{url}</link>
      <guid isPermaLink="false">7bd204c6-1655-4c27-aeee-53f933c5395f</guid>
      <pubDate>Sun, 6 Sep 2009 16:20:00 +0000</pubDate>
     </item>
     ''')

    joined_items = '\n'.join(items)

    rss_feed = f'''<?xml version="1.0" encoding="UTF-8" ?>
    <rss version="2.0">
    <channel>
     <title>Rae the Doe</title>
     <description>This is an example of an RSS feed</description>
     <link>https://comicskingdom.com/rae-the-doe</link>
     <copyright>2020 Example.com All rights reserved</copyright>
     <lastBuildDate>Mon, 6 Sep 2010 00:01:00 +0000</lastBuildDate>
     <pubDate>Sun, 6 Sep 2009 16:20:00 +0000</pubDate>
     <ttl>1800</ttl>

     {joined_items}

    </channel>
    </rss>
    '''
    open('feed.rss', 'w').write(rss_feed)
    sleep_time = int((30 + random.uniform(-2, 2)) * 60 )
    print(sleep_time)
    time.sleep(sleep_time)
