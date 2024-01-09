from rest_framework_simplejwt.authentication import JWTAuthentication


class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        """
        Custom authentication method to authenticate users based on JWT token stored in HTTP cookies.

        This method overrides the standard JWT authentication process to retrieve the JWT token
        from a HTTP-only cookie, instead of the Authorization header. It then validates the token
        to authenticate the user.

        Args:
            request: HttpRequest object containing metadata about the request.

        Returns:
            A tuple of (user, token) if authentication is successful, where 'user' is
            the user associated with the token and 'token' is the validated JWT token.
            Returns None if authentication fails, either due to missing token or validation failure.

        Raises:
            AuthenticationFailed: If the token is invalid, expired, or tampered.
        """
        # Get token from cookies (httponly)
        raw_token = request.COOKIES.get('studiosity_access_token')
        # If cookies token not found, failed authentication.
        if raw_token is None:
            return None
        # Validate token, return 
        validated_token = self.get_validated_token(raw_token)
        return self.get_user(validated_token), validated_token