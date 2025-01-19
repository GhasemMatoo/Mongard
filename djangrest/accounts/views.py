from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import UserRegisterSerializer


# Create your views here.

class UserRegister(APIView):
    serializer_class = UserRegisterSerializer

    def post(self, request, format=None):
        ser_data = self.serializer_class(data=request.POST)
        if ser_data.is_valid():
            valid_data = ser_data.validated_data
            User.objects.create_user(
                username=valid_data['username'],
                email=valid_data['email'],
                password=valid_data['password']
            )
            return Response(data=ser_data.data, status=status.HTTP_201_CREATED)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)
