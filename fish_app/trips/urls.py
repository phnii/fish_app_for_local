from django.urls import path
from .views import TripDeleteView, TripDetailView, TopView, UserTripsView, CommentDeleteView
from . import views

urlpatterns = [
  path('index/', TopView.as_view(), name="index" ),
  path('create/', views.make_inline_formset, name='create'),
  path('search/',views.search,name='search'),
  path('<int:pk>/',TripDetailView.as_view(),name='trip_detail'),
  path('<int:pk>/update/',views.update_inline_formset, name='update'),
  path('user/<int:pk>/',UserTripsView.as_view(),name='user_trips'),
  path('<int:pk>/delete/', TripDeleteView.as_view(), name='delete'),
  path('comment/<int:pk>/', CommentDeleteView.as_view(), name="comment_delete")
]