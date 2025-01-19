from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegisterSerializer


# Create your views here.

class UserRegister(APIView):
    serializer_class = UserRegisterSerializer

    def post(self, request, format=None):
        ser_data = self.serializer_class(data=request.POST)
        if ser_data.is_valid():
            valid_data = ser_data.validated_data
            ser_data.create(validated_data=valid_data)
            return Response(data=ser_data.data, status=status.HTTP_201_CREATED)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)
