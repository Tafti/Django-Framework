from django.urls import path
from django.http import HttpResponse
from . import views
from django.conf import settings
from django.conf.urls.static import static



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
    path('user-profile/<str:id>/', views.user_profile, name='user-profile'),
    path('edit-profile/<str:id>/', views.updateProfile, name='update-profile'),
]





if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)