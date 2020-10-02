from django.shortcuts import render

# Create your views here.
def home(request):
    if 'links' in request.GET:
        #fetch the details of the book
        pass
