from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Album, AlbumPhoto, Comment

class AlbumCreationForm(forms.ModelForm):

    class Meta:
        model = Album # the model this form interacts with
        fields = ['title', 'coverpic'] # makes the title and initial (cover) pic

class PhotoUploadForm(forms.ModelForm):
    # photo = forms.ImageField(label='photo')

    class Meta:
        model = AlbumPhoto
        fields = ['photo', 'caption', ]


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['body']



