from rest_framework.views import APIView
from rest_framework.response import Response
from .mixins import LoggingMixin


# Create your views here.

class Home(LoggingMixin, APIView):
    sensitive_fields = {'pass'}

    def get(self, request, *args, **kwargs):
        return Response('hello')
