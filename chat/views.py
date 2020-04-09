from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse

@login_required
def index(request):
    #return render(request, 'chat/index.html')
    return HttpResponseRedirect(reverse("chat_room", args =['principal',]))

@login_required
def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })