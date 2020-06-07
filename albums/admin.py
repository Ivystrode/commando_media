from django.contrib import admin
from .models import Album, AlbumAdmin, AlbumPhoto, AlbumPhotoAdmin, Comment, CommentAdmin

# Register your models here.
admin.site.register(Album, AlbumAdmin)
admin.site.register(AlbumPhoto, AlbumPhotoAdmin)
admin.site.register(Comment, CommentAdmin)