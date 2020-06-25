from django.shortcuts import render, redirect, Http404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, ProfileForm, UserUpdateForm, ProfileUpdateForm
from albums.models import Album, AlbumPhoto, Comment
from ideas.models import Idea, IdeaComment
from main.models import Notice, NoticeComment

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
            messages.success(request, f'Account created for {username}. Your account will now be reviewed by the administrator before you can access the site.')
            return redirect('/login')
    else:
        form = UserRegisterForm()
        d_form = ProfileForm()



    return render(request, "users/register.html", {'form':form})

@login_required()
def profile(request, username):
    if request.user.profile.approved:
        try:
            user = User.objects.get(username=username)
        except:
            raise Http404

        ideas = Idea.objects.all()
        albums = Album.objects.all()
        photos = AlbumPhoto.objects.all()

        ideacomments = IdeaComment.objects.all()
        albumcomments = Comment.objects.all()
        noticecomments = NoticeComment.objects.all()

        # editable = False

        if request.user.is_authenticated and request.user.username == user.username:
            editable = True
        else:
            editable = False
        print("user authentication status:")
        print(request.user.is_authenticated)
        print("logged in user same as this user's profile:")
        print(request.user.username == user.username)

        if editable:
            if request.method == "POST":
                u_form = UserUpdateForm(request.POST, instance=request.user)
                p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

                if u_form.is_valid() and p_form.is_valid():
                    u_form.save()
                    p_form.save()
                    messages.success(request, 'Information updated')
                    return redirect(f'/profile/{request.user.username}')
                else:
                    messages.success(request, f'Invalid request - check the username does not already exist or that you are not trying to change to an unauthorised role')
                    return redirect(f'/profile/{user.username}')

            else:
                u_form = UserUpdateForm(instance=request.user)
                p_form = ProfileUpdateForm(instance=request.user.profile)


            context = {
                'u_form':u_form,
                'p_form':p_form,
                'user':request.user,
                'ideas':ideas,
                'albums':albums,
                'photos':photos,
                'ideacomments':ideacomments,
                'albumcomments':albumcomments,
                'noticecomments':noticecomments
            }
        else:
            context = {
                'user':user,
                'ideas':ideas,
                'albums':albums,
                'photos':photos,
                'ideacomments':ideacomments,
                'albumcomments':albumcomments,
                'noticecomments':noticecomments
            }
        print("logged in user:")
        print(request.user.username)
        print("profile of:")
        print(user)
        print("editable:")
        print(editable)

        return render(request, 'users/profile.html', context)
    else:
        messages.success(request, f'You cannot access this page until your account has been approved.')
        return redirect('/')

@login_required()
def other_profile(request, username):
    user = User.objects.get(username=username)
    context = {
        'user':user
    }
    return render(request, 'users/other_profile.html', context)
