from django.shortcuts import render

# Create your views here.
def albums(request):
    return render(request, "albums/albums.html")