# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response

def signup(request):
    return HttpResponse('Hi, from signup.')