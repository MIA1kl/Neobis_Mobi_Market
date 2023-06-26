from django.shortcuts import render
from rest_framework import generics
from .serializers import RegisterSerializer, LoginSerializer, LogoutSerializer, ProfileEditSerializer, ProfileViewSerializer, PhoneVerificationSerializer, PhoneEntrySerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import User
from rest_framework import viewsets
import random
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from twilio.rest import Client
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from phonenumbers import parse, format_number, PhoneNumberFormat
from phonenumbers.phonenumberutil import NumberParseException


class RegisterView(generics.GenericAPIView):

    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data

        return Response(user_data, status=status.HTTP_201_CREATED)
    
class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    # permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class ProfileViewAPIView(generics.RetrieveAPIView):
    serializer_class = ProfileViewSerializer
    # permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'username'
    queryset = User.objects.all()


class ProfileEditAPIView(generics.UpdateAPIView):
    serializer_class = ProfileEditSerializer
    lookup_field = 'username'
    queryset = User.objects.all()

    
class PhoneEntryAPIView(generics.CreateAPIView):
    serializer_class = PhoneEntrySerializer
    lookup_field = 'username'
    def post(self, request, username):
        user = get_object_or_404(User, username=username)
        serializer = self.serializer_class(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data.get('phone_number')

        if phone_number:
            # Generate a random verification code
            verification_code = str(random.randint(1000, 9999))
            user.phone_number = phone_number
            user.verification_code = verification_code
            user.save()

            try:
                # Parse and format the phone number
                parsed_phone_number = parse(phone_number, "KG")
                formatted_phone_number = format_number(parsed_phone_number, PhoneNumberFormat.E164)

                client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
                message = client.messages.create(
                    body=f'Your verification code: {verification_code}',
                    from_=settings.TWILIO_PHONE_NUMBER,
                    to=formatted_phone_number
                )
                return Response({'status': 'success', 'message': 'SMS sent successfully.'})
            except NumberParseException:
                return Response({'status': 'error', 'message': 'Invalid phone number format.'})
            except Exception as e:
                return Response({'status': 'error', 'message': str(e)})
        else:
            return Response({'status': 'error', 'message': 'Phone number is required.'})

class PhoneVerificationAPIView(generics.CreateAPIView):
    serializer_class = PhoneVerificationSerializer

    def post(self, request, username):
        user = get_object_or_404(User, username=username)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        verification_code = serializer.validated_data['verification_code']

        if verification_code == user.verification_code:
            user.is_verified = True
            user.save()
            return Response({'message': 'Phone number verified successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Please enter the correct verification code.'}, status=status.HTTP_400_BAD_REQUEST)