import pytest

from instascrape import Profile

@pytest.fixture(scope='module')
def profile() -> Profile:
    profile_url = "https://www.instagram.com/chris_greening/"
    profile_obj = Profile(profile_url)
    profile_obj.static_load()
    return profile_obj

def test_get_recent_posts(profile):
    profile.get_recent_posts()
    assert len(profile.posts) == 12

def test_from_username(profile):

    expected_profile_username = 'chris_greening'
    result_profile: Profile = Profile.from_username(username=expected_profile_username)

    assert result_profile.name == profile.data_points[0].username
    assert result_profile.url == profile.url
