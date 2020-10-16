import pytest

from instascrape import Profile

@pytest.fixture(scope='module')
def profile() -> Profile:
    profile_url = "https://www.instagram.com/chris_greening/"
    profile_obj = Profile(profile_url)
    profile_obj.load()
    return profile_obj

def test_from_username(profile):
    expected_profile_username = 'chris_greening'
    result_profile: Profile = Profile.from_username(username=expected_profile_username)

    assert result_profile.url == profile.url
