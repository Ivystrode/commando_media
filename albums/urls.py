from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.albums, name="albums"),
    path('create_album/', views.create_album, name='create_album'),
    path('<slug>/', views.album_detail, name='album_detail'),
    path('<slug>/add_photo', views.add_photo, name='add_photo'),
    path('<slug>/<id>/', views.picture_detail, name='picture_detail'),# album_id/photo_id
]

# makemigrations wouldnt work until i changed pic_detail from id/id to id/slug
# so i may have to pretend the picture id is actually a "slug"...i guess??
