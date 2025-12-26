from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from base.models import Room
from .serializers import RoomSerializer 
from rest_framework.permissions import IsAuthenticated, AllowAny


@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/rooms/',
        'GET /api/rooms/<id>/',
        'POST /api/rooms/',
        'PUT /api/rooms/<id>/',
        'DELETE /api/rooms/<id>/',
    ]
    return Response(routes)

@api_view(['GET'])
def getRooms(request):
    rooms= Room.objects.all()
    room_values=rooms.values()
    serializer= RoomSerializer(rooms, many=True)
    return Response({"serialized_values":serializer.data[:2],"room_values":room_values[:2]})


@api_view(['GET'])
def getRoomid(request, id):
    room_by_id= Room.objects.get(id=id)
    serializer= RoomSerializer(room_by_id)
    return Response({"serialized_values":serializer.data})

@api_view(['POST'])
@permission_classes([AllowAny])  # Require login (optional)
def createRoom(request):
    """
    Create a new room
    POST /api/createRoom/
    Required: name
    Optional: description, topic, image
    """
    
    # Print for debugging
    print("User:", request.user)
    print("Data received:", request.data)
    
    # Create serializer with context (so we can access request in serializer)
    serializer = RoomSerializer(data=request.data, context={'request': request})
    
    if serializer.is_valid():
        # Save the room (host will be automatically set by serializer's create method)
        room = serializer.save()
        
        return Response({
            "success": True,
            "message": "Room created successfully",
            "room_id": room.id,
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)
    
    # If validation fails
    return Response({
        "success": False,
        "errors": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)
