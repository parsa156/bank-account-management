from django.urls import path
from .views import RegisterView, UserDetailView
urlpatterns = [
    path('signup/', RegisterView.as_view(), name='signup'),             # POST to register
    path('profile/', UserDetailView.as_view(), name='user-detail'),          # GET, PUT, DELETE authenticated user
]
