from django.urls import path
from . import views

urlpatterns = [
    path('profile/<str:username>/', views.UserProfileView.as_view(), name='user-profile'),
    #list all users
    path('list/', views.UserListView.as_view(), name='user-list'),
]
