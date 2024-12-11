from django.urls import path
from .views import RegisterView, UserDetailView, LoginView

urlpatterns = [
    path('signup/', RegisterView.as_view(), name='signup'),
    path('profile/', UserDetailView.as_view(), name='user-detail'),
    path('login/', LoginView.as_view(), name='login'),
]
