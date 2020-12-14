from instascrape.scrapers.post import Post
from instascrape.core._mappings import _IGTVMapping


class IGTV(Post):
    """Scraper for an IGTV post"""

    _Mapping = _IGTVMapping

    @staticmethod
    def _url_from_suburl(suburl: str) -> str:
        return f"https://www.instagram.com/tv/{suburl}/"
