from django.shortcuts import render, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from employeeApp.models import EventsModel
from employeeApp.serializers import EventSerialization
from .serializers import UserProfileSerializer, ForgotPasswordSerializer, ResetPasswordSerializer, CommentsSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from accountApp.models import User, EmailOTP, CommentsModel
import jwt, datetime
from .utils import send_otp_email

# Create your views here.
class Registration(APIView):
    def post(self, request):
        obj = UserProfileSerializer(data=request.data)
        obj.is_valid(raise_exception=True)
        #print(obj.errors)
        # print(obj.data)
        obj.save()
        return Response(obj.data)

class LoginView(APIView):
    def post(self, request):
        # usertype = request.data['user_type']
        email = request.data['email']
        password = request.data['password']
        # user = User.objects.filter(user_type=usertype, email=email).first()
        user = User.objects.filter(email=email).first()
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
        # token = request.COOKIES.get('access_token')
        # if not token:
        #     # If the token is expired or invalid , it raises an Authenticated exception
        #     raise AuthenticationFailed("Unauthenticated....!")
        #
        # try:
        #     # Decodes the JWT token using the secret key 'secret' and the HS256 algorithm
        #     payload = jwt.decode(token, 'access_secret', algorithms=['HS256'])
        # except jwt.ExpiredSignatureError:
        #     raise AuthenticationFailed("Unauthenticated.....!")
        # # The first() method returns the user or None if not found..!
        # user = User.objects.filter(id=payload['id']).first()
        # obj = UserProfileSerializer(user)
        # # print(obj.data)
        # return Response(obj.data)
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            raise AuthenticationFailed("Authentication credentials not provided.")

        try:
            token = auth_header.split()[1]  # Extracts the token from "Bearer <token>"
        except IndexError:
            raise AuthenticationFailed("Token format is invalid.")

        try:
            payload = jwt.decode(token, 'access_secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired.")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token.")

        user = User.objects.filter(id=payload['id']).first()
        if not user:
            raise AuthenticationFailed("User not found.")

        obj = UserProfileSerializer(user)
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


class ForgotPasswordView(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        user = User.objects.get(email=email)
        send_otp_email(user)

        return Response({"message": "OTP sent successfully to your email."}, status=status.HTTP_200_OK)


class ResetPasswordView(APIView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        otp = serializer.validated_data['otp']
        new_password = serializer.validated_data['new_password']

        try:
            user = User.objects.get(email=email)
            otp_obj = EmailOTP.objects.filter(user=user).last()

            if not otp_obj:
                return Response({"error": "OTP not found."}, status=status.HTTP_400_BAD_REQUEST)

            if otp_obj.is_expired():
                return Response({"error": "OTP has expired."}, status=status.HTTP_400_BAD_REQUEST)

            if otp_obj.otp != otp:
                return Response({"error": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()
            return Response({"message": "Password changed successfully."}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_400_BAD_REQUEST)


# liking and unliking evens api
class LikeEventsAPI(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, event_id):
        event = get_object_or_404(EventsModel, id=event_id)
        serializer = EventSerialization(event)
        if event.liked_by.filter(
                id=request.user.id).exists():
            event.liked_by.remove(request.user)
            return Response({
                "status":"success",
                "message":"You unliked this posted event!",
                "events":serializer.data,
                "total_likes":event.liked_by.count()
            }, status=status.HTTP_200_OK)
        event.liked_by.add(request.user)
        return Response({
            "status":"success",
            "message":"You liked this posted event!",
            "events":serializer.data,
            "total_likes":event.liked_by.count()
        }, status=status.HTTP_200_OK)

class CommentsAPI(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, event_id):
        event = get_object_or_404(EventsModel, id=event_id)
        comment_obj = CommentsSerializer(data=request.data)
        if comment_obj.is_valid():
            comment_obj.save(user_id=request.user, event_id=event)
            event_serializer = EventSerialization(event)
            return Response({
                "status":"succees",
                "message":"Your comment has been posted!",
                "events":event_serializer.data,
                "comments":comment_obj.data
            }, status=status.HTTP_200_OK)
        return Response({
            "status":"failed",
            "message":"failed to post your comment!",
            "errors":comment_obj.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class ModifyComments(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, comment_id):
        comment = get_object_or_404(CommentsModel, id=comment_id)
        if request.user != comment.user_id:
            return Response({
                "status":"failed",
                "message":"Only owner can edit this comment!"
            }, status=status.HTTP_401_UNAUTHORIZED)
        else:
            edited_comment = CommentsSerializer(
                instance=comment,
                data=request.data,
                partial=True
            )
            if edited_comment.is_valid():
                edited_comment.save()
                return Response({
                    "status":"success",
                    "message":"Comment updated successfully!",
                    "edited comment":edited_comment.data
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "status":"failed",
                    "message":"Failed to update comment!"
                }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, comment_id):
        comment = get_object_or_404(CommentsModel, id=comment_id)
        if request.user != comment.user_id and request.user != comment.event_id.user:
            return Response({
                "status":"failed",
                "message":"Only owner can delete this comment!"
            }, status=status.HTTP_401_UNAUTHORIZED)
        else:
            comment.delete()
            return Response({
                "status":"success",
                "message":"Comment deleted successfully!"
            }, status=status.HTTP_200_OK)