from dj_rest_auth.jwt_auth import JWTCookieAuthentication
from django.conf import settings

class CustomCookieAuthentication(JWTCookieAuthentication):
    """
    An authentication plugin that hopefully authenticates requests through a JSON web
    token provided in a request cookie (and through the header as normal, with a
    preference to the header).

    2 cookies are recieved, one containing the signature and the other the payload.
        Signature Cookie: HTTPOnly, SameSite, Secure
        Header + Payload Cookie: SameSite, Secure 
    """
    def authenticate(self, request):
        return super().authenticate(request)
    
    def authenticate(self, request):
        payload_cookie_name = getattr(settings, 'JWT_PAYLOAD_COOKIE_NAME', None)
        signature_cookie_name = getattr(settings, 'JWT_SIGNATURE_COOKIE_NAME', None)

        header = self.get_header(request)
        if header is None:
            if payload_cookie_name and signature_cookie_name:
                header_payload = request.COOKIES.get(payload_cookie_name)
                signature = request.COOKIES.get(signature_cookie_name)
                if header_payload is None or signature is None:
                    raw_token = None
                else:
                    raw_token = f"{header_payload}.{signature}"

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
    
    
