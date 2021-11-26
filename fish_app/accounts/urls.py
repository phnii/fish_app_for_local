from django.urls import path
from . import views
from .views import SignupView, UserUpdateView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('update/<int:pk>/', UserUpdateView.as_view(), name='user_update'),
]