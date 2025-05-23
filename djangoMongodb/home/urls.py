from django.urls import path
from home import views

app_name = 'home'
urlpatterns = [
    path('', views.HomeView.as_view(), name="home"),
    path('questions/', views.QuestionListView.as_view(), name="questions"),
    path('question/create/', views.QuestionCreateView.as_view(), name="questions_create"),
    path('question/update/<int:pk>/', views.QuestionUpdateView.as_view(), name="questions_update"),
    path('question/delete/<int:pk>/', views.QuestionDeleteView.as_view(), name="questions_delete"),
]
