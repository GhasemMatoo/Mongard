from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Person
from .serialaizers import PersonSerializer
# Create your views here.


class HomeView(APIView):
    serializer_class = PersonSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        person = Person.objects.all()
        data = self.serializer_class(instance=person, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)
