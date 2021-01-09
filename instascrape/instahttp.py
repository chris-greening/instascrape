import requests 

headers_template = {
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36 Edg/87.0.664.66",
    "cookies": 'ig_did=D6062989-79DC-4895-8F51-70E3A3140928; ig_nrcb=1; mid=X7xJawALAAFH0ZaxODxpBmYQ7FS9; fbm_124024574287414=base_domain=.instagram.com; shbid=10250; shbts=1609871507.7187707; rur=PRN; csrftoken=rTEqOoZxAdE89QGigWzQeWE8vSxKuker; ds_user_id=8318756192; sessionid=8318756192%3AmOfpeYw6MBn3EA%3A28; fbsr_124024574287414=GU0kWfnn-Elx_ajFCKXf4cR9wg8DOeEBNLeNF70w5FI.eyJ1c2VyX2lkIjoiMTAwMDAxMjc5NTIzOTczIiwiY29kZSI6IkFRQjNKTFdxZDVnS0lJWDdrMnRTRE1WZ3NPQks5ZDh1TkZMQnpQc0I4SnVhZmR6V28wUHoweHlnd2FCZGNtZ2pWZTlzZFBuMklWdi01c3VzWTczYlFqdU1RcmhlbmhJa1dTSDdicHlCV1dianNBaF9EQkREN2dVcG5kaEZZOTJ0Q3N3eFpzYWx6YnhlU0ZDS2s1LXRDNmNaaGVUaUw3Rlo5UVliR1RxZEFBY3RwU1hkeGM1WUJtQUV5YUdmRS1zZldWalZXWnpiaEVDLUw1M0JaUGVCOVZUTEJ4QzRDeVhWOXRmMEpaYlJNUDU1OEdBdWY3b29WX1NISVp6aDRyb1V1VmhwVnVIaVhKRWt5cU5pOGxBYUhuV1FrTnNKTUNhUGlMbFBRTmQ0SmZ6c1FCNVd2X0pEdE9EcjY2bHpETlBCVGFtMXpEc2JLLW5MRHVRTUVGYkd1eFlBIiwib2F1dGhfdG9rZW4iOiJFQUFCd3pMaXhuallCQVBrZjBaQkFjNFJ6azN1NXV6S1BZMG1VWkJ5NXAyMTBnZTR5ek4zWFVVN3FzYzJqeTVmWGZIVGtva2xFS09XZk4zNzlkZDZwaFpCVUYxZGx3WkFOSWJ3WkNkSWI2QXBlQ1ZQZnRyRkpNaFpDQjJVeW5ZOVVWTWZRVE1EOUhieFpDMFQ2aldpR2JsVnM4MTdzSDJkSnhUUFhrWkNXaVpCalZZaHdTZG5Ocmk2NFpDVGJaQkZ4U2FJWEQwWkQiLCJhbGdvcml0aG0iOiJITUFDLVNIQTI1NiIsImlzc3VlZF9hdCI6MTYxMDA3Nzc1MX0; urlgen="{\"67.245.173.176\": 12271}:1kxivo:aGnPggc9nHr67XHdcIt9_8-YSZE'
}

class InstaSession(requests.Session):
    def get(self, *args, headers=headers_template, **kwargs):
        return super().get(*args, **kwargs, headers=headers)

if __name__ == '__main__':
    with InstaSession() as session:
        resp = session.get("https://www.instagram.com/")
