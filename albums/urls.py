from django.urls import path, include
from . import views
# from .views import AlbumListView

urlpatterns = [
    path('', views.albums, name="albums"), # comment out when using below method
    # path('', AlbumListView.as_view(), name="albums"), # class based one
    path('create_album/', views.create_album, name='create_album'),
    path('<slug>/', views.album_detail, name='album_detail'),
    path('<slug>/delete', views.delete_album, name="delete_album"),
    path('<slug>/edit_album', views.edit_album, name="edit_album"), 
    path('<slug>/add_photo', views.add_photo, name='add_photo'),
    path('<slug>/<id>/', views.picture_detail, name='picture_detail'),# album_id/photo_id
    path('<slug>/<id>/delete', views.delete_picture, name="delete_picture"),
    path('<slug>/<id>/edit_picture', views.edit_picture, name="edit_picture"), 
]

# makemigrations wouldnt work until i changed pic_detail from id/id to id/slug
# so i may have to pretend the picture id is actually a "slug"...i guess??
