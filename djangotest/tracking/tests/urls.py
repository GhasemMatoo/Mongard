from django.urls import path
from . import views as test_views

app_name = 'tracking'
urlpatterns = [
    path('no-logging/', test_views.MockNologgingView.as_view(), name='no-logging'),
    path('logging/', test_views.MockLoggingView.as_view(), name='logging')
]
