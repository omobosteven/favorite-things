from rest_framework_simplejwt import authentication
from rest_framework import HTTP_HEADER_ENCODING


class CookieAuthentication(authentication.JWTAuthentication):

    def get_header(self, request):
        header = request.COOKIES.get('jwt_token')

        if isinstance(header, str):  # pragma: no branch
            # Work around django test client oddness
            header = header.encode(HTTP_HEADER_ENCODING)

        return header
