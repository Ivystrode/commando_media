from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, DetailsForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        d_form = DetailsForm(request.POST)
        if form.is_valid() and d_form.is_valid():
            user = form.save()
            d_form = d_form.save(commit=False)
            d_form.user = user
            d_form.save()

            username = form.cleaned_data.get('username')
            print(form.cleaned_data)
            messages.success(request, f'Account created for {username}')
            return redirect('login')
    else:
        form = UserRegisterForm()
        d_form = DetailsForm()
    


    return render(request, "users/register.html", {'form':form})

@login_required()
def profile(request):
    return render(request, 'users/profile.html')