from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            access_token = response.data['access']
            refresh_token = response.data['refresh']
            #TODO add , secure=True for https only
            response.set_cookie(
                key='access_token', value=access_token, httponly=True, samesite='Lax'
            )
            response.set_cookie(
                key='refresh_token', value=refresh_token, httponly=True, samesite='Lax'
            )
        return response

@api_view(['POST'])
def logout_view(request):
    response = JsonResponse({'detail': 'Successfully logged out.'})
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')
    return response