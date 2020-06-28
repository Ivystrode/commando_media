from django import forms
from django.contrib.auth.models import User
from .models import Notice, NoticeComment, CustomEmailMessage

class NoticeCreationForm(forms.ModelForm):

    image = forms.ImageField(required=False)

    class Meta:
        model = Notice
        fields = ['title', 'image', 'body']

class NoticeCommentForm(forms.ModelForm):

    class Meta:
        model = NoticeComment
        fields = ['body']

class DeleteNoticeForm(forms.ModelForm):

    model = Notice

class EditNoticeForm(forms.ModelForm):
    
    image = forms.ImageField(required=False)

    class Meta:
        model = Notice
        fields = ['title', 'image', 'body']

class CustomEmailForm(forms.ModelForm):


    class Meta:
        model = CustomEmailMessage
        fields = ['sender_email', 'subject', 'body']