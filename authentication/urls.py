from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import RegisterView

urlpatterns = [
    path('signup/', RegisterView.as_view(), name='signup'),  
]
