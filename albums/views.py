from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import AlbumCreationForm, PhotoUploadForm, CommentForm
from .models import Album, AlbumPhoto, Comment
from django.contrib import messages

# Create your views here.
@login_required()
def albums(request):
    albums = Album.objects.all()
    context = {'albums':albums}
    return render(request, "albums/albums.html", context)


@login_required()
def create_album(request):    
    if request.method == "POST":
        form = AlbumCreationForm(request.POST, request.FILES)
        if form.is_valid():
            new_album = form.save(commit=False)
            print("save no commit")

            new_album.created_by = request.user

            print(new_album.created_by)

            new_album.save()

            print("saved")

            albumname = form.cleaned_data.get('title')
            print(form.cleaned_data)
            messages.success(request, f'Album created: {albumname}')
            return redirect('/albums')
    else:
        form = AlbumCreationForm()

    return render(request, "albums/create_album.html", {'form':form})

@login_required()
def album_detail(request, id):
    return render(request, "albums/album_detail.html")

@login_required()
def picture_detail(request, id, slug):
    return render(request, "albums/picture_detail.html")