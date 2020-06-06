from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.albums, name="albums"),
    path('<id>/', views.album_detail, name='album_detail'),
    path('<id>/<id>/', views.picture_detail, name='picture_detail'),# album_id/photo_id
]