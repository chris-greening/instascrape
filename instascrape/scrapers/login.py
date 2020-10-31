from instascrape.core._mappings import _LoginMapping
from instascrape.core._static_scraper import _StaticHtmlScraper


class LoginAndSignupPage(_StaticHtmlScraper):
    _Mapping = _LoginMapping

    def _construct_url(self):
        pass
