from django.urls import path
from . import views
from .models import Room, Topic, Messages
from .forms import RoomForm, UserForm
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout
from django.contrib.auth.views import LogoutView
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required




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
            auth_login(request, user)  
            if request.user.is_authenticated:
                messages.success(request, f"Welcome back, {user.email or user.email}!")
            return redirect('home')
        else:
            # Login failed
            messages.error(request, "Invalid username or password.")
            return render(request, 'base/login.html')
    return render(request, 'base/login.html')  


def logout_view(request):
    if request.method == 'POST':
        storage = messages.get_messages(request)
        storage.used = True  
    
        logout(request)
        messages.success(request, "You have been successfully logged out.")
        return redirect('login')  
    
    return redirect('home')

def user_profile(request, id):
    user = User.objects.get(id=id)
    user_rooms= Room.objects.filter(host=user)
    topics = Topic.objects.filter(room__host=user).distinct()
    messaged_rooms = Room.objects.filter(messages__user=user).distinct()
    messages= Messages.objects.filter(user=user)
    context = {'user': user, 'user_rooms': user_rooms, 'topics': topics, 'messages': messages, 'messaged_rooms': messaged_rooms}
    return render(request, 'base/userprofile.html', context)

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
            user = form.save(commit=False)
            user.email = form.cleaned_data.get('email').lower() 
            user.username = user.email  # Set username to email
            user.save()
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
    messages_data = Messages.objects.filter(room=rooms_data).order_by('-created')
    # participants = rooms_data.participants.all()
    users_with_messages = User.objects.filter(messages__room=rooms_data).distinct() 


    if request.method == 'POST':
    
        body = request.POST.get('body')
        
        rooms_data.has_uploaded_image = bool(rooms_data.image and hasattr(rooms_data.image, 'url'))
        
        Messages.objects.create(
            room=rooms_data,
            user=request.user,
            body=body
        )
        return redirect('room', id=int(id))
    
    context = {'room': rooms_data, 'comments': messages_data, 'participants': users_with_messages}
    return render(request, 'base/room.html', context)       

def rooms(request):
    rooms_data = Room.objects.all()
    context = {'rooms': rooms_data}
    return render(request, 'base/rooms.html', context)


def posts(request):
    return render(request, 'base/post.html')


# def create_room(request):
#     if request.method == 'POST':
#         form = RoomForm(request.POST, request.FILES)  # Important: include FILES
#         if form.is_valid():
#             room = form.save()
#             # Process image here if needed
#             return redirect('room', pk=room.pk)
#     else:
#         form = RoomForm()
#     return render(request, 'create_room.html', {'form': form})

# def room_detail(request, pk):
#     room = get_object_or_404(Room.objects.prefetch_related('images'), pk=pk)
#     return render(request, 'room_detail.html', {'room': room})


def createRoom(request):
    # Only authenticated users can create rooms
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.method == 'POST':
        # CRITICAL: Include BOTH request.POST AND request.FILES
        form = RoomForm(request.POST, request.FILES)
        
        if form.is_valid():
            # Don't save directly - set the host first
            room = form.save(commit=False)
            room.host = request.user
            
            # Save to get an ID
            room.save()
            
            # Save ManyToMany relationships if any
            form.save_m2m()
            
            # Debug: Check if image was uploaded
            if 'image' in request.FILES:
                print(f"DEBUG: Image uploaded: {request.FILES['image'].name}")
                print(f"DEBUG: Image saved to: {room.image}")
            else:
                print("DEBUG: No image uploaded")
            
            # Redirect to the NEWLY CREATED room, not home
            return redirect('room', id=room.id)  # ← FIX: Use room.id
            
        else:
            # Form has errors - show them
            print(f"Form errors: {form.errors}")
    else:
        # GET request - create empty form
        form = RoomForm()
    
    context = {'form': form}
    return render(request, 'base/room_form.html', context)



# def createRoom(request):
#     form = RoomForm(request.POST, request.FILES)
#     context = {'form': form}  
#     if request.method == 'POST':
#         print(request.POST)
#         form = RoomForm(request.POST)
        
#         if form.is_valid():
#             form.save()
#             return redirect('home')  
#     return render(request, 'base/room_form.html', context)


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
    

@login_required(login_url='login')
def updateProfile(request, id):
    
    user = User.objects.get(id=id)
    form = UserForm(instance=user)
    context = {'form': form}  
    if request.user != user:
        messages.error(request, "You can only edit your own profile!")
        return redirect('home')
    if request.method == 'POST':
        print(request.POST)
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('home')  
    return render(request, 'base/edit-profile.html', context)
