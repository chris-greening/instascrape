class JSONKeyError(Exception):
    def __init__(self, key, *args, **kwargs):
        msg = f"'{key}' could not be found in Instagram's JSON data"
        super().__init__(msg, *args, **kwargs)
