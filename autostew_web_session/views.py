from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return list(request)

def list(request):
    return HttpResponse("Session list")