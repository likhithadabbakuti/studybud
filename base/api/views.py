# from django.http import JsonResponse #format of data 
from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room
from .serializers import RoomSerializers
from base.api import serializers

@api_view(['GET']) # VIEW CAN TAKE THE HTTP METHODS
def getRoutes(request):#show all routes in api
    routes=[
        'GET /api', #home page
        'GET /api/rooms',#get all rooms in app
        'GET /api/rooms/:id',#single room
    ]
    return Response(routes) 

@api_view(['GET'])
def getRooms(request):
    rooms=Room.objects.all()
    serializer = RoomSerializers(rooms, many=True) #for many obj
    return Response(serializer.data) #we don't need obj to return so to return data we use .data

@api_view(['GET'])
def getRoom(request,pk):#for single room
    room=Room.objects.get(id = pk)
    serializer = RoomSerializers(room, many=False)
    return Response(serializer.data)