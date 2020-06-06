from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.
class Album(models.Model):
    # id should be randomly generated - default is incremental, make sure to do it randomly
    title = models.CharField(max_length=50)
    coverpic = models.ImageField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='albums')
    # slug = models.SlugField() use ID to recall album instead?
    time = models.DateTimeField(default=timezone.now())

    class Meta:
        ordering = ['-time']

    def photos(self):
        photo_list = [pic.photo.name for pic in self.photos.all()]
        return photo_list

    def __str__(self):
        return self.id + ": " + self.title

class AlbumAdmin(admin.ModelAdmin):
    search_fields = ['title', 'created_by']
    list_display = ['title', 'created_by']


class AlbumPhoto(models.Model):
    # id should be randomly generated - default is incremental, make sure to do it randomly
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='photos')
    photo = models.ImageField(upload_to=f'albums/{album.id}')
    thumb = models.ImageField(upload_to=f'albums/{album.id}/thumbs')
    caption = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_photos')
    time = models.DateTimeField(default=timezone.now())

    def thumbnail(self): # must be called no each image at upload time/form post

        img = Image.open(self.thumb.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.thumb.path)

    class Meta:
        ordering = ['-time']

    def __str__(self):
        return self.id + ": " + self.caption


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