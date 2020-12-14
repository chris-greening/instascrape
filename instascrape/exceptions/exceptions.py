class InstagramLoginRedirectError(Exception):
    """
    Exception that indicates Instagram is redirecting away from the page
    that should be getting scraped. Can be remedied by logging into Instagram.
    """

    def __init__(
        self,
        message="Instagram is redirecting you to the login page instead of the page you are trying to scrape. This could be occuring because you 1. made too many requests too quickly or 2. are not logged into Instagram on your machine.",
    ):
        super().__init__(message)


class WrongSourceError(Exception):
    """
    Exception that indicates user passed the wrong source type to the scraper.
    An example is passing a URL for a hashtag page to a Profile.
    """

    def __init__(self, message="Wrong input source, use the correct class"):
        super().__init__(message)
