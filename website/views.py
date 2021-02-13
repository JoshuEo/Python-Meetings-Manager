from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse

from meetings.models import Meeting

def welcome(request):
    return render(request, "website/welcome.html", {"meetings": Meeting.objects.all()}) # Dictionary


def date(request):
    return HttpResponse("This page was served at " + str(datetime.now()))


def about(request):
    return HttpResponse("My name is Joshua Eom. Welcome to my first webpage using Django!")
