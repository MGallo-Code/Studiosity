from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            access_token = response.data['access']
            refresh_token = response.data['refresh']
            response.set_cookie(
                key='lifelocker_access_token',
                value=access_token,
                httponly=True,
                samesite='Strict',
                secure=True
            )
            response.set_cookie(
                key='lifelocker_refresh_token',
                value=refresh_token,
                httponly=True,
                samesite='Strict',
                secure=True
            )
        return response


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('lifelocker_refresh_token')
        if not refresh_token:
            raise ValidationError('No refresh token provided')
        
        request.data._mutable = True
        request.data.update({'refresh': refresh_token})

        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            access_token = response.data['access']
            response.set_cookie(
                key='lifelocker_access_token',
                value=access_token,
                httponly=True,
                samesite='Strict',
                secure=True
            )
        return response

@api_view(['POST'])
def logout_view(request):
    response = JsonResponse({ "detail": "Logged out successfully." })
    response.delete_cookie('lifelocker_access_token')
    response.delete_cookie('lifelocker_refresh_token')
    return response