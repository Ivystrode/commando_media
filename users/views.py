from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, ProfileForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.
def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        d_form = ProfileForm(request.POST)
        if form.is_valid() and d_form.is_valid():
            user = form.save()
            d_form = d_form.save(commit=False)
            d_form.user = user
            d_form.save()

            username = form.cleaned_data.get('username')
            print(form.cleaned_data)
            messages.success(request, f'Account created for {username}')
            return redirect('/')
    else:
        form = UserRegisterForm()
        d_form = ProfileForm()
    


    return render(request, "users/register.html", {'form':form})

@login_required()
def profile(request, username):
    try:
        user = User.objects.get(username=username)
    except:
        raise Http404
    
    # editable = False

    if request.user.is_authenticated == True and request.user.username == user.username:
        editable = True
    else:
        editable = False

    print(request.user.is_authenticated)
    print(request.user.username == user.username)

    if editable == True:
        if request.method=="POST":
            u_form = UserUpdateForm(request.POST, instance=request.user)
            p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
            if u_form.is_valid() and p_form.is_valid():
                u_form.save()
                p_form.save()
                messages.success(request, 'Information updated')
                return redirect('/profile')
        else:
            u_form = UserUpdateForm(instance=request.user)
            p_form = ProfileUpdateForm(instance=request.user.profile)


        context = {
            'u_form':u_form,
            'p_form':p_form,
            'user':request.user
        }
    else:
        context = {
            'user':user
        }
    print(request.user.username)
    print(user)
    print(editable)

    return render(request, 'users/profile.html', context)

@login_required()
def other_profile(request, username):
    user = User.objects.get(username=username)
    context = {
        'user':user
    }
    return render(request, 'users/other_profile.html', context)