import pytest

from instascrape import LoginAndSignupPage


@pytest.fixture
def login_page():
    url = r"https://www.instagram.com/accounts/login/"

    login_page = LoginAndSignupPage(url=url)
    login_page.load()
    return login_page


def test_login(login_page):
    assert login_page.url == login_page.url
