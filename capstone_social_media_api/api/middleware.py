import jwt
from django.conf import settings
from django.http import HttpResponse

class DisableCSRFForAPI:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/api/'):  # Adjust prefix if needed
            setattr(request, '_dont_enforce_csrf_checks', True)
        return self.get_response(request)


# class JWTCSRFExemptMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         if 'Authorization' in request.headers and request.headers['Authorization'].startswith('Bearer '):
#             token = request.headers['Authorization'].split(' ')[1]
#             try:
#                 jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
#                 return self.get_response(request)
#             except jwt.ExpiredSignatureError:
#                 return HttpResponse('Token has expired', status=401)
#             except jwt.InvalidTokenError:
#                 return HttpResponse('Invalid token', status=401)
#         return self.get_response(request)