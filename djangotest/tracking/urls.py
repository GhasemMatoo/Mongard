from django.urls import path,include
from . import views

app_name = 'tracking'
urlpatterns = [
    # path("", views.Home.as_view()),
    path('', include('tracking.tests.urls', namespace='test')),
]
