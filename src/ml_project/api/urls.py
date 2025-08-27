from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    # URL for the API endpoint
    path('api/predict/', views.PredictView.as_view(), name='predict_api'),
    # URL for the frontend
    path('', views.frontend_view, name='frontend'),
]

urlpatterns = format_suffix_patterns(urlpatterns)