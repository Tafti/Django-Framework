from django.urls import path
from . import views
from .models import Room, Topic, Messages
from .forms import RoomForm
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout
from django.contrib.auth.views import LogoutView
from .forms import CustomUserCreationForm




def login(request):

    if request.method == 'POST':
        username= request.POST.get('username')
        password= request.POST.get('password')
        # Validate inputs
        if not username or not password:
            messages.error(request, "Please enter both username and password.")
            return render(request, 'base/login.html')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Login successful
            auth_login(request, user)  # Note: using auth_login to avoid naming conflict
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('home')
        else:
            # Login failed
            messages.error(request, "Invalid username or password.")
            return render(request, 'base/login.html')
    return render(request, 'base/login.html')  # ← THIS WAS MISSING!


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')  # or 'home'
    # If GET request, redirect to home or show confirmation
    return redirect('home')

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    if q:
        rooms_data = Room.objects.filter(
        Q(topic__name__icontains=q)|
        Q(name__icontains=q) |
        Q(description__icontains=q)
        )
    else:
        rooms_data = Room.objects.all()
    room_count = len(rooms_data)
    topic = Topic.objects.all()
    context = {'rooms': rooms_data, 'topics': topic, 'room_count': room_count}
    return render(request, 'base/home.html', context)

def register(request):
    # If user is already logged in, redirect to home
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Auto-login after registration (optional)
            auth_login(request, user)
            
            messages.success(request, f'Account created for {user.username}! You are now logged in.')
            return redirect('home')
        else:
            # Form has errors
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'base/register.html', {'form': form})
def room(request, id):
    rooms_data = Room.objects.get(id=id)
    context = {'room': rooms_data}
    return render(request, 'base/room.html', context)       

def rooms(request):
    rooms_data = Room.objects.all()
    context = {'rooms': rooms_data}
    return render(request, 'base/rooms.html', context)


def posts(request):
    return render(request, 'base/post.html')

def createRoom(request):
    form = RoomForm()
    context = {'form': form}  
    if request.method == 'POST':
        print(request.POST)
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  
    return render(request, 'base/room_form.html', context)


def updateRoom(request, id):
       
        room = Room.objects.get(id=id)
        form = RoomForm(instance=room)
        context = {'form': form}  
        if request.method == 'POST':
            print(request.POST)
            form = RoomForm(request.POST, instance=room)
            if form.is_valid():
                form.save()
                return redirect('home')  
        return render(request, 'base/room_form.html', context)



def deleteRoom(request, id):
    try:
        room = get_object_or_404(Room, id=id)
        
        # Optional: Check if user has permission to delete
        # if request.user != room.host:
        #     messages.error(request, "You can only delete rooms you created!")
        #     return redirect('home')
        
        if request.method == 'POST':
            room.delete()
            messages.success(request, f"Room '{room.name}' deleted successfully!")
            return redirect('home')
        
        context = {'room': room}
        return render(request, 'base/delete.html', context)
        
    except Exception as e:
        messages.error(request, f"Error: {str(e)}")
        return redirect('home')