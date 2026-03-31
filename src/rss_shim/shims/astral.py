"""Shim for the blog of Astral, the company that develops Ruff."""

from dataclasses import dataclass
import datetime as dt
import re
from typing import ClassVar, cast

from bs4 import BeautifulSoup
import requests

from rss_shim.feed_gen import RssFeed, RssFeedItem
from rss_shim.shims.base_shim import BaseShim
from rss_shim.utils import get_logger

logger = get_logger(__name__)


@dataclass
class AstralShim(BaseShim):
    """Shim for the blog of Astral, the company that develops Ruff."""

    blog_url: ClassVar[str] = "https://astral.sh/blog"

    @property
    def shim_path(self) -> str:
        """Location for files within the data directory."""
        return "astral"

    def generate_feed(self) -> RssFeed:
        """Generate an RSS feed, retrieving data as needed.

        Returns:
            An instantiated RssFeed object.
        """
        response = requests.get(self.blog_url, timeout=30)
        response.raise_for_status()
        page_text = response.text

        soup = BeautifulSoup(page_text, features="html.parser")
        blog_div = soup.find("div", attrs={"id": "Blog"})
        if blog_div is None:
            raise ValueError(
                f"Blog URL {self.blog_url!r} does not contain `<div>` with `id` of `Blog`"
            )
        blog_posts = blog_div.find_all("a", attrs={"href": True})
        items = []
        for blog_post in blog_posts:
            blog_title_element = blog_post.find("h3", attrs={"class": "text-h5"})
            if blog_title_element is None:
                raise ValueError(f"Cannot find blog title element in {self.blog_url!r}")
            blog_title = blog_title_element.text
            blog_description_element = blog_post.find("p", attrs={"class": "body-m text-comet"})
            if blog_description_element is None:
                raise ValueError(f"Cannot find blog description element in {self.blog_url!r}")
            blog_description = blog_description_element.text
            blog_url = cast(str, blog_post["href"])

            blog_date_element = blog_post.find("p", attrs={"class": "subtitle text-comet"})
            if blog_date_element is None:
                raise ValueError(f"Cannot find blog date element in {self.blog_url!r}")
            blog_date = blog_date_element.text
            blog_date = re.sub(r"\s+", " ", blog_date.strip())
            pub_date = dt.datetime.strptime(blog_date, "%B %d, %Y").replace(tzinfo=dt.UTC)

            items.append(
                RssFeedItem(
                    title=blog_title,
                    description=blog_description,
                    link=blog_url,
                    pub_date=pub_date,
                )
            )

        feed = RssFeed(
            title="Astral Blog",
            description="Recent blog posts from Astral",
            link=self.blog_url,
            url=self.feed_url,
            items=items,
        )
        return feed
