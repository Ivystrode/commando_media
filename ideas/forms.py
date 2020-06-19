from django import forms
from django.contrib.auth.models import User
from .models import Idea, IdeaComment

class IdeaCreationForm(forms.ModelForm):

    image = forms.ImageField(required=False)

    class Meta:
        model = Idea
        fields = ['title', 'image', 'body']

class IdeaCommentForm(forms.ModelForm):

    class Meta:
        model = IdeaComment
        fields = ['body']

class DeleteIdeaForm(forms.ModelForm):

    model = Idea

class EditIdeaForm(forms.ModelForm):
    
    image = forms.ImageField(required=False)

    class Meta:
        model = Idea
        fields = ['title', 'image', 'body']