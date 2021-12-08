from django.urls import path
from .views import FollowListView, RoomDetailView, SignupView, UserUpdateView, follow, message_create, room_create, unfollow

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('update/<int:pk>/', UserUpdateView.as_view(), name='user_update'),
    path('follow-list/<int:pk>/', FollowListView.as_view(), name='follow_list'),
    path('follow/<int:pk>/', follow, name='follow'),
    path('unfollow/<int:pk>/', unfollow, name='unfollow'),
    path('room-create/<int:pk>/', room_create, name='room_create'),
    path('room/<int:pk>/', RoomDetailView.as_view(), name='room_detail'),
    path('message/<int:pk>/', message_create, name='message_create')
]