from rest_framework.views import APIView
from rest_framework.response import Response
from tracking.mixins import LoggingMixin


class MockNologgingView(APIView):
    def get(self, request, *args, **kwargs):
        return Response('on logging')


class MockLoggingView(LoggingMixin, APIView):
    def get(self, request, *args, **kwargs):
        return Response('with logging')
