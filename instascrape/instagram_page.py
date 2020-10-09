from abc import ABC 

class InstagramPage(ABC):
    """
    Basic building blocks of Instagram are pages. These pages are specialized
    further into hashtag pages, profile pages, post pages, etc.
    """
    def __init__(self, name: str):
        self.name = name

        #Separate scrapes
        self.data_points = []

