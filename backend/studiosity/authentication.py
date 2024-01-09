from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom view to handle JWT token obtainment through HTTP-only cookies.

    This view overrides the standard token obtainment behavior of TokenObtainPairView
    to set the access and refresh tokens in HTTP-only cookies, enhancing the security
    by not exposing tokens to client-side JavaScript.
    """

    def post(self, request, *args, **kwargs):
        """
        Custom view to handle JWT token obtainment through HTTP-only cookies.

        This view overrides the standard token obtainment behavior of TokenObtainPairView
        to set the access and refresh tokens in HTTP-only cookies, enhancing the security
        by not exposing tokens to client-side JavaScript.
        """
        # Validate login request by calling parent class's post method
        response = super().post(request, *args, **kwargs)
        # If the login is successful, set cookies with access and refresh tokens
        if response.status_code == 200:
            access_token = response.data['access']
            refresh_token = response.data['refresh']
            response.set_cookie(
                key='studiosity_access_token',
                value=access_token,
                httponly=True,
                samesite='Strict',
                secure=True
            )
            response.set_cookie(
                key='studiosity_refresh_token',
                value=refresh_token,
                httponly=True,
                samesite='Strict',
                secure=True
            )
        return response


class CustomTokenRefreshView(TokenRefreshView):
    """
    Custom view for refreshing JWT tokens, using the refresh token from HTTP-only cookies.

    This view extends the standard TokenRefreshView behavior to retrieve the refresh token
    from an HTTP-only cookie instead of expecting it in the request body or headers.
    """

    def post(self, request, *args, **kwargs):
        """
        Handle POST request to refresh JWT access token using a refresh token from cookies.

        Args:
            request: HttpRequest object.

        Returns:
            HttpResponse object with the new access token set in cookies if the refresh is successful.
            Raises ValidationError if the refresh token is not provided or invalid.
        """
        # Validate refresh token from cookies
        refresh_token = request.COOKIES.get('studiosity_refresh_token')
        if not refresh_token:
            raise ValidationError('No refresh token provided')
        
        # Necessary to update the request's data
        request.data._mutable = True
        # Add the refresh token with the correct name for our super() call
        request.data.update({'refresh': refresh_token})
        # Call super() to refresh our token,
        #   now that it's been retrieved from cookies and properly set in the headers
        response = super().post(request, *args, **kwargs)

        # If successful, set the new access token cookie.
        if response.status_code == 200:
            access_token = response.data['access']
            response.set_cookie(
                key='studiosity_access_token',
                value=access_token,
                httponly=True,
                samesite='Strict',
                secure=True
            )
        return response

@api_view(['POST'])
def logout_view(request):
    """
    API view to log out a user by deleting JWT tokens stored in HTTP-only cookies.

    Deletes 'studiosity_access_token' and 'studiosity_refresh_token' cookies to log the user out.

    Args:
        request: HttpRequest object.

    Returns:
        JsonResponse indicating successful logout.
    """
    response = JsonResponse({ "detail": "Logged out successfully." })
    response.delete_cookie('studiosity_access_token')
    response.delete_cookie('studiosity_refresh_token')
    return response