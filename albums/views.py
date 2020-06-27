from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .forms import *
from django.forms import modelformset_factory
from .models import Album, AlbumPhoto, Comment

from django.contrib import messages
from django.utils.text import slugify
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView

# Create your views here.
@login_required()
def albums(request):
    if request.user.profile.approved:
        albums = Album.objects.all()
        context = {'albums':albums}
        return render(request, "albums/albums.html", context)
    else:
        messages.success(request, f'You cannot access this page until your account has been approved.')
        return redirect('/')

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
    if request.user.profile.approved:
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

                # new_photo = AlbumPhoto.objects.create(album=new_album, photo=new_album.coverpic, thumb=new_album.coverpic, caption='Album Cover', created_by=request.user)
                new_photo = AlbumPhoto.objects.create(album=new_album, photo=new_album.coverpic, caption='Album Cover', created_by=request.user)
                new_photo.save()

                print("saved")

                albumname = form.cleaned_data.get('title')
                print(form.cleaned_data)
                messages.success(request, f'Album created: {albumname}')
                return redirect('/albums')
        else:
            form = AlbumCreationForm()

        return render(request, "albums/create_album.html", {'form':form})
    else:
        messages.success(request, f'You cannot access this page until your account has been approved.')
        return redirect('/')

@login_required()
def album_detail(request, slug):
    if request.user.profile.approved:
        album = Album.objects.get(slug=slug)
        # comment_count = picture.comments.count()
        return render(request, "albums/album_detail.html", {'album': album})
    else:
        messages.success(request, f'You cannot access this page until your account has been approved.')
        return redirect('/')

@login_required()
def picture_detail(request, id, slug):
    if request.user.profile.approved:
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
    else:
        messages.success(request, f'You cannot access this page until your account has been approved.')
        return redirect('/')

@login_required()
def delete_album(request, slug):
    if request.user.profile.approved:
        album_to_delete = Album.objects.get(slug=slug)
        context = {'album':album_to_delete}
        if request.method == "POST":
            if request.user == album_to_delete.created_by or request.user.profile.staff:
                print("deleted" + str(album_to_delete.title))
                album_to_delete.delete()
                print("deleted")
                messages.success(request, f'Album deleted')
                return redirect('/albums')
            else:
                messages.success(request, f'You may only delete albums if you are the creator or HQ staff')
                return redirect(f'/albums')
        return render(request, "albums/delete_album.html", context)
    else:
        messages.success(request, f'You cannot access this page until your account has been approved.')
        return redirect('/')

@login_required()
def edit_album(request, slug):
    if request.user.profile.approved:
        print("EDIT ROUTE")
        album = Album.objects.get(slug=slug)
        if request.user == album.created_by or request.user.profile.staff:
            if request.method == "POST":
                form = EditAlbumForm(request.POST, request.FILES, instance=album)
                if form.is_valid():
                    edited_album = form.save(commit=False)
                    print("form cleaned data")
                    print(form.cleaned_data)
                    print("edited idea")
                    print(edited_album)
                    edited_album.slug = slugify(edited_album.title)# slugify(form.cleaned_data('title'))
                    edited_album.save()
                    messages.success(request, f'Edits saved to: {edited_album.title}')
                    return redirect(f'/albums/{album.slug}')
            
            else:
                existing_data = {'title':album.title, 'coverpic': album.coverpic}
                form = EditAlbumForm(initial=existing_data)
        else:
            print("not staff user")
            messages.success(request, f'You may only edit this post if you are the creator or HQ staff')
            return render(request, "albums/album_detail.html", {'album':album})

        return render(request, "albums/edit_album.html", {'form':form, 'album':album})
    else:
        messages.success(request, f'You cannot access this page until your account has been approved.')
        return redirect('/')




@login_required()
def add_photo(request, slug):
    if request.user.profile.approved:
        album = Album.objects.get(slug=slug)

        PhotoFormSet = modelformset_factory(AlbumPhoto, form=PhotoUploadForm, extra=5)

        if request.method == "POST":
            formset = PhotoFormSet(request.POST, request.FILES, queryset=AlbumPhoto.objects.none())

            if formset.is_valid():

                for form in formset.cleaned_data:
                    if form:
                        # photo = form['photo']

                        # new_photo = AlbumPhoto(album = Album.objects.get(slug=slug), photo = form['photo'], thumb = form['photo'], created_by = request.user, caption=form['caption'])
                        new_photo = AlbumPhoto(album = Album.objects.get(slug=slug), photo = form['photo'], created_by = request.user, caption=form['caption'])
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
    else:
        messages.success(request, f'You cannot access this page until your account has been approved.')
        return redirect('/')


@login_required()
def delete_picture(request, slug, id):
    if request.user.profile.approved:
        picture_to_delete = AlbumPhoto.objects.get(id=id)
        album = Album.objects.get(slug=picture_to_delete.album.slug)
        context = {'picture':picture_to_delete, 'album':album}
        if request.method == "POST":
            if request.user == picture_to_delete.created_by or request.user.profile.staff:
                print("deleted" + str(picture_to_delete.caption))
                picture_to_delete.delete()
                print("deleted")
                messages.success(request, f'Photo deleted')
                return redirect(f'/albums/{album.slug}')
            else:
                messages.success(request, f'You may only delete photos if you are the creator or HQ staff')
                return redirect(f'/albums/{album.slug}/{picture_to_delete.id}')
        return render(request, 'albums/delete_picture.html', context)
    else:
        messages.success(request, f'You cannot access this page until your account has been approved.')
        return redirect(f'/albums/{album.slug}')

@login_required()
def edit_picture(request, slug, id):
    if request.user.profile.approved:
        print("EDIT ROUTE")
        picture = AlbumPhoto.objects.get(id=id)
        album = Album.objects.get(slug=slug)
        if request.user == picture.created_by or request.user.profile.staff:
            if request.method == "POST":
                form = EditPictureForm(request.POST, request.FILES, instance=picture)
                if form.is_valid():
                    edited_picture = form.save(commit=False)
                    print("form cleaned data")
                    print(form.cleaned_data)
                    print("edited picture")
                    print(edited_picture)
                    edited_picture.save()
                    messages.success(request, f'Edits saved to: {edited_picture.caption}')
                    return redirect(f'/albums/{album.slug}/{picture.id}')
            
            else:
                existing_data = {'caption':picture.caption, 'photo': picture.photo}
                form = EditPictureForm(initial=existing_data)
                # return render(request, 'albums/edit_picture.html', {'picture':picture, 'album':album})
        else:
            print("not staff user")
            messages.success(request, f'You may only edit this post if you are the creator or HQ staff')
            return render(request, "albums/picture_detail.html", {'picture':picture, 'album':album})

        return render(request, "albums/edit_picture.html", {'form':form, 'picture':picture, 'album':album})
    else:
        messages.success(request, f'You cannot access this page until your account has been approved.')
        return redirect('/')