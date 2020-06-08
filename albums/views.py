from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .forms import AlbumCreationForm, PhotoUploadForm, CommentForm
from django.forms import modelformset_factory
from .models import Album, AlbumPhoto, Comment

from django.contrib import messages
from django.utils.text import slugify
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView

# Create your views here.
@login_required()
def albums(request):
    albums = Album.objects.all()
    context = {'albums':albums}
    return render(request, "albums/albums.html", context)

# ======CLASS BASED VERSION OF ALBUMS HTML (ABOVE)=====
# Doesn't make much, if any difference. Will stick with function view type for this page.

# @method_decorator(login_required, name='dispatch')
# class AlbumListView(ListView):
#     model = Album
#     template_name = 'albums/albums.html'
#     context_object_name = 'albums'
#     ordering = ['title']


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
            # return HttpResponseRedirect('') # clear form on submission
            return redirect(f'/albums/{album.slug}/{picture.id}')
    else:
        form = CommentForm()

    return render(request, "albums/picture_detail.html", {'picture':picture, 'album':album, 'form':form})

@login_required()
def add_photo(request, slug):
    album = Album.objects.get(slug=slug)

    PhotoFormSet = modelformset_factory(AlbumPhoto, form=PhotoUploadForm, extra=5)

    if request.method == "POST":
        formset = PhotoFormSet(request.POST, request.FILES, queryset=AlbumPhoto.objects.none())

        if formset.is_valid():

            for form in formset.cleaned_data:
                if form:
                    # photo = form['photo']

                    new_photo = AlbumPhoto(album = Album.objects.get(slug=slug), photo = form['photo'], thumb = form['photo'], created_by = request.user, caption=form['caption'])
                    # print("Saved: " + new_photo.caption)
                    # new_photo.save()

                    # new_photo = form.save(commit=False)
                    # new_photo.album = Album.objects.get(slug=slug)
                    # new_photo.thumb = new_photo.photo
                    # new_photo.created_by = request.user

                    # print("Picture upload data stored in variable")

                    # print(form.cleaned_data)

                    # print("form data on line above this")

                    new_photo.save()
                    print(f"saved {new_photo.caption} to {new_photo.album.title}")
            return redirect(f'/albums/{album.slug}')
        else:
            print(formset.errors)

    else:
        formset = PhotoFormSet(queryset=AlbumPhoto.objects.none())

    return render(request, "albums/add_photo.html", {'album':album, 'formset':formset})