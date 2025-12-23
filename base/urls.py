from django.urls import path
from django.http import HttpResponse
from . import views




urlpatterns = [
    

    path('login/', views.login, name='login'),   
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('', views.home, name='home'),
    path('room/<str:id>/', views.room, name='room'),
    path('rooms/', views.rooms, name='rooms'),
    path('posts/', views.posts, name='posts'),
    path('create-room/', views.createRoom, name='create-room'),
    path('update-room/<str:id>/', views.updateRoom, name='update-room'),
    path('delete-room/<str:id>/', views.deleteRoom, name='delete-room'),
]
