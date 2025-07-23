from django.shortcuts import render
from .serializers import UserProfileSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from accountApp.models import User
import jwt, datetime

# Create your views here.

class Registration(APIView):
    def post(self, request):
        obj = UserProfileSerializer(data=request.data)
        obj.is_valid(raise_exception=True)
        # print(obj.data)
        obj.save()
        return Response(obj.data)

class LoginView(APIView):
    def post(self, request):
        usertype = request.data['user_type']
        email = request.data['email']
        password = request.data['password']
        user = User.objects.filter(user_type=usertype, email=email).first()
        if user is None:
            raise AuthenticationFailed("User not found")
        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password")

        access_payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }
        refresh_payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
            'iat': datetime.datetime.utcnow()
        }

        access_token = jwt.encode(access_payload, 'access_secret', algorithm='HS256')
        refresh_token = jwt.encode(refresh_payload, 'refresh_secret', algorithm='HS256')

        response = Response()

        response.set_cookie(key='access_token', value=access_token, httponly=True)
        response.set_cookie(key='refresh_token', value=refresh_token, httponly=True)

        response.data = {
            'access': access_token,
            'refresh': refresh_token
        }
        return response


class UserView(APIView):
    def get(self, request):
        # Retrieves the JWT token from the request's cookies.if no token is found.
        # It raises an Authentication exception , indicating that the user is unauthenticated.
        token = request.COOKIES.get('access_token')
        if not token:
            # If the token is expired or invalid , it raises an Authenticated exception
            raise AuthenticationFailed("Unauthenticated....!")
        try:
            # Decodes the JWT token using he secret key 'secret' and the HS256 algorithm
            payload = jwt.decode(token, 'access_secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated.....!")
        # The first() method returns the user or None if not found..!
        user = User.objects.filter(id=payload['id']).first()
        obj = UserProfileSerializer(user)
        # print(obj.data)
        return Response(obj.data)

class RefreshTokenView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            raise AuthenticationFailed("Refresh token missing")

        try:
            payload = jwt.decode(refresh_token, 'refresh_secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Refresh token expired")

        new_access_payload = {
            'id': payload['id'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=15),
            'iat': datetime.datetime.utcnow()
        }
        new_access_token = jwt.encode(new_access_payload, 'access_secret', algorithm='HS256')

        response = Response()
        response.set_cookie(key='access_token', value=new_access_token, httponly=True)
        response.data = {
            'access': new_access_token
        }
        return response


class UserLogout(APIView):
    def post(self, request):
        x = Response()
        x.delete_cookie('access_token')
        x.delete_cookie('refresh_token')
        x.data = {
            "Message": "Successfully logout...!"
        }
        return x


