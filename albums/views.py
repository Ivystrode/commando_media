from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import AlbumCreationForm, PhotoUploadForm, CommentForm
from .models import Album, AlbumPhoto, Comment
from django.contrib import messages
from django.utils.text import slugify
from django.http import HttpResponse, HttpResponseRedirect

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
            new_album.slug = slugify(form.cleaned_data.get('title'))

            print(new_album.created_by)
            print(form.cleaned_data)
            print(new_album)

            new_album.save()

            new_photo = AlbumPhoto.objects.create(album=new_album, photo=new_album.coverpic, thumb=new_album.coverpic, caption='Album Cover', created_by=request.user)
            new_photo.save()

            print("saved")

            albumname = form.cleaned_data.get('title')
            print(form.cleaned_data)
            messages.success(request, f'Album created: {albumname}')
            return redirect('/albums')
    else:
        form = AlbumCreationForm()

    return render(request, "albums/create_album.html", {'form':form})

@login_required()
def album_detail(request, slug):
    album = Album.objects.get(slug=slug)
    # comment_count = picture.comments.count()
    return render(request, "albums/album_detail.html", {'album': album})

@login_required()
def picture_detail(request, id, slug):
    picture = AlbumPhoto.objects.get(id=id)
    album = Album.objects.get(slug=slug)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            print("posting new comment")
            #create comment object but dont save to db yet
            new_comment = form.save(commit=False)
            print("comment picked up")
            #assign current article to the comment
            new_comment.parent = picture
            print("comment assigned to picture")
            new_comment.author = request.user
            #save comment to db
            new_comment.save()
            print("comment saved!")
            return HttpResponseRedirect('') # clear form on submission
            return redirect('/albums')
    else:
        form = CommentForm()

    return render(request, "albums/picture_detail.html", {'picture':picture, 'album':album, 'form':form})

@login_required()
def add_photo(request, slug):
    album = Album.objects.get(slug=slug)

    if request.method == "POST":
        form = PhotoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            new_photo = form.save(commit=False)
            new_photo.album = Album.objects.get(slug=slug)
            new_photo.thumb = new_photo.photo
            new_photo.created_by = request.user

            print("Picture upload data stored in variable")

            print(form.cleaned_data)

            print("form data on line above this")

            new_photo.save()
            print(f"saved {new_photo.caption} to {new_photo.album.title}")
            return redirect(f'/albums/{album.slug}')

    else:
        form = PhotoUploadForm()

    return render(request, "albums/add_photo.html", {'album':album, 'form':form})