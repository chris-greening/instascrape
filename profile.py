class Profile:
    def __init__(self, url):
        self.url = url
    
    def load(self):
        """Load the static HTML into a BeautifulSoup object at the url"""
        self.page_source = requests.get(self.url).text
        self.soup = BeautifulSoup(self.page_source, features='lxml')

        self._scrape_soup()

    def _scrape_soup(self):
        """Scrape data from the soup"""
        pass

    @classmethod 
    def from_username(cls, username):
        url = f'https://www.instagram.com/{username}/'
        return cls(url)

if __name__ == '__main__':
    url = r'https://www.instagram.com/chris_greening/'
    profile = Profile(url)