class Profile:
    def __init__(self, url):
        self.url = url
    
    @classmethod 
    def from_username(cls, username):
        url = f'https://www.instagram.com/{username}/'
        return cls(url)

if __name__ == '__main__':
    url = r'https://www.instagram.com/chris_greening/'
    profile = Profile(url)