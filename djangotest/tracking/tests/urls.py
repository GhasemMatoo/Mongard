from django.urls import path
from . import views as test_views

app_name = 'tracking'
urlpatterns = [
    path('no-logging/', test_views.MockNologgingView.as_view(), name='no-logging'),
    path('logging/', test_views.MockLoggingView.as_view(), name='logging'),
    path('explicit-logging/', test_views.MockExplicitLoggingView.as_view(), name='explicit_logging'),
    path('custom-check-logging/', test_views.MockCustomCheckLoggingView.as_view(), name='custom_check_logging'),
    path('session-auth-logging/', test_views.MockSessionAuthLoggingView.as_view(), name='session_auth_logging'),
    path('token-auth-logging/', test_views.MockTokenAuthLoggingView.as_view(), name='token_auth_logging'),
    path('invalid-cleaned-substitute-logging/',
         test_views.MockInvalidCleandSubstitutedFieldsLoggingView.as_view(), name='invalid_cleaned_substitute_logging'),
    path('sensitive-fields-logging/',
         test_views.MockSensitiveFieldsLoggingView.as_view(), name='sensitive_fields_logging'),
]
