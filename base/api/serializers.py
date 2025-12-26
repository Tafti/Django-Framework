# from rest_framework.serializers import ModelSerializer
# from base.models import Room


# class RoomSerializer(ModelSerializer):
#     class Meta:
#         model = Room
#         fields = '__all__'



from rest_framework import serializers
from base.models import Room, Topic
from django.contrib.auth.models import User

class RoomSerializer(serializers.ModelSerializer):
    # For foreign key fields, you might want to show more details
    host = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), 
        required=False  # Make host optional in POST
    )
    topic = serializers.PrimaryKeyRelatedField(
        queryset=Topic.objects.all(), 
        required=False  # Make topic optional
    )
    
    class Meta:
        model = Room
        fields = [
            'id', 'host', 'name', 'description', 
            'participants', 'updated', 'created', 
            'topic', 'image'
        ]
        read_only_fields = ['id', 'updated', 'created', 'participants']
    
    def create(self, validated_data):
        # Get the current user from request context
        request = self.context.get('request')
        
        # Set host to current user if not provided
        if 'host' not in validated_data and request and request.user.is_authenticated:
            validated_data['host'] = request.user
        
        return super().create(validated_data)