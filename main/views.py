from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.
@login_required()
def home(request):


    context = {'user': request.user}
    print(request.user)


    return render(request, "main/home.html", context)

def notices(request):


    context = {'user': request.user}
    print(request.user)


    return render(request, "main/notices.html", context)