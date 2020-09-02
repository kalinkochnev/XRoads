"""
class CustomCookieAuth(JWTCookieAuthentication):
    
    An authentication plugin that hopefully authenticates requests through a JSON web
    token provided in a request cookie (and through the header as normal, with a
    preference to the header).
    

    def authenticate(self, request):
        cookie_name = getattr(settings, 'JWT_AUTH_COOKIE', None)
        header = self.get_header(request)
        if header is None:
            if cookie_name:
                raw_token = request.COOKIES.get(cookie_name)
                if getattr(settings, 'JWT_AUTH_COOKIE_ENFORCE_CSRF_ON_UNAUTHENTICATED', False): #True at your own risk 
                    self.enforce_csrf(request)
                elif raw_token is not None and getattr(settings, 'JWT_AUTH_COOKIE_USE_CSRF', False):
                    self.enforce_csrf(request)
            else:
                return None
        else:
            raw_token = self.get_raw_token(header)

        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)
        return self.get_user(validated_token), validated_token
"""
"""Login View
- If user credentials are valid, return empty body and set 2 cookies
    - Session cookie with JWT signature
    - Permanent cookie with JWT payload
- If credentials invalid, return form errors and bad response status code
"""

"""Auth for requests
- Read the 2 cookies
- Put them together

"""