# custom_authentication.py

from rest_framework_simplejwt.authentication import JWTAuthentication

class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # Get the token from the cookies. Assume it's stored under 'access_token'
        raw_token = request.COOKIES.get('lifelocker_access_token')
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)

        return self.get_user(validated_token), validated_token
