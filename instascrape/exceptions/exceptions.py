class InstagramLoginRedirectError(Exception):
    def __init__(self, message="Instagram is redirecting you to the login page. Login to Instagram on your machine and try again"):
        super().__init__(message)