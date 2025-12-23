from django.db import models
from django.contrib.auth.models import User



class Room(models.Model):

    host = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    participants = models.CharField(max_length=200, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)               
    created = models.DateTimeField(auto_now_add=True)
    topic = models.ForeignKey('Topic', on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return str(self.name)

class Topic(models.Model):

    name = models.CharField(max_length=200)
    hashtag = models.CharField(max_length=100, null=True, blank=True)   


    def __str__(self):
        return str(self.name)
    

class Messages(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True)
    body = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)               
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return str(self.body[:50])
