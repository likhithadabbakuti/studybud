from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Room,Topic,Message
from .forms import RoomForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
# rooms =[
#     {'id':1,'name':'let us learn python'},
#     {'id':2, 'name':'design with me'},
#     {'id':3, 'name':'Frontend developers'},
# ]
def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        #give u,p
        username = request.POST.get('username')
        password = request.POST.get('password')
        #check if user exist
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,'User does not exist')
        #credentials are crct
        user = authenticate(request, username=username, password=password)
        #create session and allow to login
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'username or password does not exist')
    context={'page':page}
    return render(request,'base/login_register.html',context)
def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    page = 'register'
    form = UserCreationForm()
    #pass the user data
    if request.method == 'POST':
        form = UserCreationForm(request.POST) #through in UCform
        if form.is_valid():
            user=form.save(commit=False)
            #commit = false -saving and freezing the user
            user.username = user.username.lower() #get un which is lowercase
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'An error occured during registration')
    return render(request,'base/login_register.html',{'form':form})
def home(request):
    #to get query like if we click on one topic that topic related info
    q=request.GET.get('q') if request.GET.get('q') != None else ''
    rooms=Room.objects.filter(Q(topic__name__icontains=q)|
                             Q(name__icontains=q)|
                              Q(description__icontains=q) )
    #only topic name _ _ for parent
    #icontains-matches the data if substr exists, contains-will be case-sensitive
    room_count= rooms.count()
    topics = Topic.objects.all()
    room_messages=Message.objects.all()
    context={'rooms':rooms,'topics':topics,'room_count':room_count,'room_messages':room_messages}
    return render(request,'base/home.html',context) 

def room(request,pk):
    room=Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created')
    participants=room.participants.all()

    if request.method == 'POST':
        message=Message.objects.create(
            user=request.user, 
            room = room,
            body=request.POST.get('body'),
        )
        room.participants.add(request.user)
        return redirect('room',pk=room.id)
    
    context={'room':room,'room_messages':room_messages,'participants':participants}

    return render(request,'base/room.html',context)

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save() 
            return redirect('home')
    context = {'form':form}
    return render(request, 'base/room_form.html',context)

@login_required(login_url='login')
def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.user != room.host:
        return HttpResponse('you are not allowwed here!!')
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context={'form':form}
    return render(request,'base/room_form.html',context)

@login_required(login_url='login')
def deleteRoom(request,pk):
    room =Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse('you are not allowwed here!!')
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':room})

@login_required(login_url='login')
def deleteMessage(request,pk):
    message =Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse('you are not allowwed here!!')
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':message})
