from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib import admin
from PIL import Image

# Create your models here.

# callback function to create media folder for album's coverpic
def coverpic_path(instance, filename):
    return '/'.join(['albums', instance.title, filename])
class Album(models.Model):
    # id should be randomly generated - default is incremental, make sure to do it randomly
    title = models.CharField(max_length=50)
    coverpic = models.ImageField(upload_to=coverpic_path)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='albums')
    slug = models.SlugField()
    time = models.DateTimeField(default=timezone.now())

    class Meta:
        ordering = ['-time']

    # def photos(self):
    #     photo_list = [pic.photo.name for pic in self.photos.all()]
    #     return photo_list trying to list all photos in album

    def __str__(self):
        return str(self.id) + ": " + str(self.title)

class AlbumAdmin(admin.ModelAdmin):
    search_fields = ['title', 'created_by']
    list_display = ['title', 'created_by']

# callback function to create media folder for album's photos
def album_folder(instance, filename):
    print("ALBUM DIRECTORY FUNCTION")
    parent_album = Album.objects.get(title=instance.album.title)
    print(str(parent_album))
    album_name = parent_album.title
    print(album_name)
    return '/'.join(['albums/', album_name, filename])

def thumb_folder(instance, filename):
    print("THUMB DIRECTORY FINDER")
    parent_album = Albums.objects.get(id=self.album.id)
    print(str(parent_album))
    album_name = parent_album.slug
    print(album_name)
    return '/'.join(['albums/', album_name, '/thumbs/', filename])

class AlbumPhoto(models.Model):   
    # id should be randomly generated - default is incremental, make sure to do it randomly
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='photos')
    photo = models.ImageField(upload_to=album_folder)
    thumb = models.ImageField(upload_to=thumb_folder)
    caption = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_photos')
    time = models.DateTimeField(default=timezone.now())



    # def save(self): # must be called no each image at upload time/form post
    #     super().save()

    #     img = Image.open(self.thumb.path)

    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)
    #         img.save(self.thumb.path)

    class Meta:
        ordering = ['-time']

    def __str__(self):
        return str(self.id) + ": " + str(self.caption)


class AlbumPhotoAdmin(admin.ModelAdmin):
    search_fields = ['album', 'caption', 'time', 'created_by']
    list_display = ['album', 'time', 'created_by']






class Comment(models.Model):
    parent = models.ForeignKey(AlbumPhoto, on_delete=models.CASCADE,related_name='comments')
    author = models.CharField(max_length=80)
    body = models.TextField()
    time = models.DateTimeField(default=timezone.now())

    class Meta:
        ordering = ['time']

        def __str__(self):
            return f'Comment by {self.author}: {self.body}'

class CommentAdmin(admin.ModelAdmin):
    search_fields = ['author']
    list_display = ['author', 'time']