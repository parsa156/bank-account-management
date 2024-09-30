from django.urls import path
from .views import RegisterView, UserDetailView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('signup/', RegisterView.as_view(), name='signup'),             # POST to register
    path('profile/', UserDetailView.as_view(), name='user-detail'),          # GET, PUT, DELETE authenticated user
]
