from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from django.contrib.auth import authenticate
from user.serializers import UserSerializer, UserLoginSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.settings import api_settings


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        response_data = {
            'email': serializer.data['email'],
            'firstname': serializer.data['firstname'],
            'lastanme': serializer.data['lastname'],
            'message': 'Welcome, registration successfully'
        }

        response = Response(response_data, status=status.HTTP_201_CREATED)
        expiration = (datetime.utcnow() +
                      api_settings.ACCESS_TOKEN_LIFETIME)
        response.set_cookie('access_token',
                            serializer.data['token'],
                            expires=expiration,
                            secure=True,
                            httponly=True)
        return response


class LoginUserView(generics.CreateAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny, )

    def create(self, request, *args, **kwargs):
        password = request.data.get('password', '')
        email = request.data.get('email', '')

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(request, username=email.strip(), password=password.strip(), **kwargs)

        if user is not None:
            response_data = {
                'message': 'Welcome back, Login successfully'
            }
            response = Response(response_data, status=status.HTTP_200_OK)
            expiration = (datetime.utcnow() +
                          api_settings.ACCESS_TOKEN_LIFETIME)
            response.set_cookie('jwt_token',
                                serializer.data['token'],
                                expires=expiration,
                                secure=True,
                                httponly=True)
            return response

        response_data = {
            'message': 'Wrong email or password'
        }
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
