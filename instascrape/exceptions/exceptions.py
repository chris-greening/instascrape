class InstagramLoginRedirect(Exception):
    def __init__(self, message="You do not have valid cookies. Login to Instagram on your machine and try again"):
        super().__init__(message)