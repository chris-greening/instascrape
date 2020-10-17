from instascrape.core._static_scraper import _StaticHtmlScraper
from instascrape.core._mappings import _LoginMapping


class LoginAndSignupPage(_StaticHtmlScraper):
    _Mapping = _LoginMapping
