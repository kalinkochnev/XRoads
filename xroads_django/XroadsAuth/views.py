from dj_rest_auth.views import LoginView, LogoutView
from django.conf import settings
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from XroadsAuth.serializers import CustomLoginSerializer


# Create your views here.
def email_confirm_success(request):
    return render(request, 'email_success.html')


class CustomLoginView(LoginView):
    serializer_class = CustomLoginSerializer

    def bake_cookies(self, response):
        # This creates the cookies to be sent back to the client 
        payload_cookie_name = settings.JWT_PAYLOAD_COOKIE_NAME
        signature_cookie_name = settings.JWT_SIGNATURE_COOKIE_NAME

        token_str = str(self.access_token)
        header_payload_key = '.'.join(token_str.split('.')[:2])
        signature_key = token_str.split('.')[-1]

        from datetime import timezone, datetime
        expiration = (datetime.now(tz=timezone.utc) + settings.ACCESS_TOKEN_LIFETIME)
        
        # Creates Payload cookie name (permanent cookie)
        response.set_cookie(
            payload_cookie_name,
            header_payload_key,
            expires=expiration,
            secure=False,
            samesite='Strict'
        )
        # FIXME make secure = to TRUE in production

        # Creates Signature cookie name (normally session cookie, unless remember login)
        signature_kwargs = {
            'secure': False,
            'httponly': True,
            'samesite': 'Strict',
        }
        if self.serializer.validated_data['remember_me']:
            signature_kwargs['expires'] = expiration

        response.set_cookie(
            signature_cookie_name,
            signature_key,
            **signature_kwargs
        )
        # FIXME make secure = to TRUE in production


    def get_response(self):
        serializer_class = self.get_response_serializer()

        if getattr(settings, 'REST_USE_JWT', False):
            data = {
                'user': self.user,
                'access_token': self.access_token,
                'refresh_token': self.refresh_token
            }
            serializer = serializer_class(instance=data,
                                          context=self.get_serializer_context())
        else:
            serializer = serializer_class(instance=self.token,
                                          context=self.get_serializer_context())

        response = Response(serializer.data, status=status.HTTP_200_OK)
        self.bake_cookies(response)
        
        return response

class CustomLogoutView(LogoutView):
    pass