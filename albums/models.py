from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib import admin

from PIL import Image
import uuid
from stdimage import StdImageField
from dynamic_filenames import FilePattern
from datetime import datetime
import random, os

#==========MODEL FUNCTIONS==========

def coverpic_path(instance, filename):
    return '/'.join(['albums', instance.slug, filename])

def album_folder(instance, filename):
    print("ALBUM DIRECTORY FUNCTION")

    base_filename, file_extension = os.path.splitext(filename)
    dt = datetime.now().strftime("%Y%m%d%H%M")
    nums = '1234567890'
    randomid = ''.join((random.choice(nums)) for x in range(3))

    print("datetime string: " + str(dt))
    print("random id: " + str(randomid))

    new_filename = f'{randomid}{dt}'
    parent_album = Album.objects.get(title=instance.album.title)
    print(str(parent_album))
    album_name = parent_album.slug
    print("saving:")
    print(new_filename)
    print("to")
    print(album_name)
    return '/'.join(['albums/', album_name, new_filename + file_extension])

# dont think this is used any more
def thumb_folder(instance, filename):

    print("THUMB DIRECTORY FINDER")
    parent_album = Album.objects.get(id=instance.album.id)
    print(str(parent_album))
    album_name = parent_album.slug
    print(album_name)
    return '/'.join(['albums/', album_name, '/thumbs/', filename])

#==========FILENAMING==========
# does this replace the above functions...?
# photo_name_pattern = FilePattern(
#     filename_pattern = '{albums}/{AlbumPhoto}'
# )


#==========MODELS==========

class Album(models.Model):
    title = models.CharField(max_length=50)
    # coverpic = models.ImageField(upload_to=coverpic_path)
    coverpic = StdImageField(upload_to=coverpic_path, variations = {'thumbnail': {'width': 300, 'height': 300, 'crop':False}})
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='albums')
    slug = models.SlugField()
    time = models.DateTimeField(default=timezone.localtime(timezone.now()))

    class Meta:
        ordering = ['-time']

    def __str__(self):
        return str(self.id) + ": " + str(self.title)


class AlbumPhoto(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='photos')
    # photo = models.ImageField(upload_to=album_folder)

    # thumb = models.ImageField(upload_to=thumb_folder)

    photo = StdImageField(upload_to=album_folder, variations = {'thumbnail': {'width': 300, 'height': 300, 'crop':False}})
    # stdimage allows standardized file renaming and thumbnail creation
    # figure out how to use the thumbnail...
    # can replace the thumb = models.imagefield above this block

    caption = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_photos')
    time = models.DateTimeField(default=timezone.localtime(timezone.now()))

    class Meta:
        ordering = ['-time']

    def __str__(self):
        return str(self.id) + ": " + str(self.caption)

class Comment(models.Model):
    # need to give comments a UUID as well? maybe also for users??
    parent = models.ForeignKey(AlbumPhoto, on_delete=models.CASCADE,related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='albumphotocomments')
    body = models.TextField()
    time = models.DateTimeField(default=timezone.localtime(timezone.now()))

    class Meta:
        ordering = ['-time']

        def __str__(self):
            return f'Comment by {self.author}: {self.body}'

#==========MODEL ADMIN==========

class CommentAdmin(admin.ModelAdmin):
    search_fields = ['author']
    list_display = ['author', 'time']

class CommentAdminInline(admin.TabularInline):
    model = Comment

class AlbumPhotoAdmin(admin.ModelAdmin):
    search_fields = ['album', 'caption', 'time', 'created_by']
    list_display = ['album', 'time', 'created_by']
    inlines = [CommentAdminInline]

class AlbumPhotoInline(admin.TabularInline):
    model = AlbumPhoto

class AlbumAdmin(admin.ModelAdmin):
    search_fields = ['title', 'created_by']
    list_display = ['title', 'created_by']
    inlines = [AlbumPhotoInline]



