
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BankAccountViewSet , BankViewSet

router = DefaultRouter()
router.register(r'accounts', BankAccountViewSet)
router.register(r'banks', BankViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
