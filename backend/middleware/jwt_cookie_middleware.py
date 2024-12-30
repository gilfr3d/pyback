from django.utils.deprecation import MiddlewareMixin

class JwtCookieMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if isinstance(response.data, dict) and 'access' in response.data:
            response.set_cookie(
                key='access_token',
                value=response.data['access'],
                httponly=True,
                secure=True,
                samesite='Strict',
            )
        if isinstance(response.data, dict) and 'refresh' in response.data:
            response.set_cookie(
                key='refresh_token',
                value=response.data['refresh'],
                httponly=True,
                secure=True,
                samesite='Strict',
            )
        return response
