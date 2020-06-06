from django.contrib import admin

# Register your models here.
admin.site.register(Album, AlbumAdmin)
admin.site.register(AlbumPhoto, AlbumPhotoAdmin)
admin.site.register(Comment, CommentAdmin)