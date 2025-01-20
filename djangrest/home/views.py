from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Person, Question, Answer
from .serialaizers import PersonSerializer, QuestionSerializer, AnswerSerializer
from permissions import IsOwnerOrReadOnly


# Create your views here.


class HomeView(APIView):
    serializer_class = PersonSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        person = Person.objects.all()
        data = self.serializer_class(instance=person, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)


class QuestionListView(APIView):
    serializer_class = QuestionSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        questions = Question.objects.all()
        srz_data = self.serializer_class(instance=questions, many=True)
        return Response(data=srz_data.data, status=status.HTTP_200_OK)
    #
    # def post(self, request, *args, **kwargs):
    #     srz_data = self.serializer_class(data=request.data)
    #     srz_data.is_valid(raise_exception=True)
    #     srz_data.save()
    #     return Response(data=srz_data.data, status=status.HTTP_201_CREATED)
    #
    # def put(self, request, *args, **kwargs):
    #     question = Question.objects.get(pk=kwargs.get('pk'))
    #     srz_data = self.serializer_class(instance=question, data=request.data, partial=True)
    #     srz_data.is_valid(raise_exception=True)
    #     srz_data.save()
    #     return Response(data=srz_data.data, status=status.HTTP_202_ACCEPTED)
    #
    # def delete(self, request, *args, **kwargs):
    #     try:
    #         question = Question.objects.get(pk=kwargs.get('pk'))
    #         question.delete()
    #         return Response(data={'message': 'question deleted'}, status=status.HTTP_202_ACCEPTED)
    #     except Question.DoesNotExist:
    #         return Response(status=status.HTTP_400_BAD_REQUEST)


class QuestionCreateView(APIView):
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        srz_data = self.serializer_class(data=request.data)
        srz_data.is_valid(raise_exception=True)
        srz_data.save()
        return Response(data=srz_data.data, status=status.HTTP_201_CREATED)


class QuestionUpdateView(APIView):
    serializer_class = QuestionSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def put(self, request, *args, **kwargs):
        question = Question.objects.get(pk=kwargs.get('pk'))
        self.check_permissions(request, question)
        srz_data = self.serializer_class(instance=question, data=request.data, partial=True)
        srz_data.is_valid(raise_exception=True)
        srz_data.save()
        return Response(data=srz_data.data, status=status.HTTP_202_ACCEPTED)


class QuestionDeleteView(APIView):
    serializer_class = QuestionSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def delete(self, request, *args, **kwargs):
        try:
            question = Question.objects.get(pk=kwargs.get('pk'))
            question.delete()
            return Response(data={'message': 'question deleted'}, status=status.HTTP_202_ACCEPTED)
        except Question.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
