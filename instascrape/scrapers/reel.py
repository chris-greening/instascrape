from instascrape.scrapers.post import Post
from instascrape.core._mappings import _ReelMapping


class Reel(Post):
    """Scraper for an Instagram reel"""

    _Mapping = _ReelMapping

    @staticmethod
    def _url_from_suburl(suburl: str) -> str:
        return f"https://www.instagram.com/reel/{suburl}/"
