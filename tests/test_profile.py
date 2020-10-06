from instascrape import Profile


def test_from_username():
    expected_profile_usename = "instagram"
    expected_profile_url = f"https://www.instagram.com/{expected_profile_usename}/"

    result_profile: Profile = Profile.from_username(username=expected_profile_usename)

    assert result_profile.name == expected_profile_usename
    assert result_profile.url == expected_profile_url
