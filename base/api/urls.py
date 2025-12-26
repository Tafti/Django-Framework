from django.urls import path
from . import views


urlpatterns = [    
    
    path('', views.getRoutes, name='api-overview'),
    path('rooms/', views.getRooms, name='api-rooms'),
    path('rooms/<str:id>/', views.getRoomid, name='api-room-id'),
    path('createRoom/', views.createRoom, name='api-create-room'),
  
         
]


