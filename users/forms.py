from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Details

class UserRegisterForm(UserCreationForm):
    role = forms.ChoiceField(choices=Details.roles, required=True)
    email = forms.EmailField()

    class Meta:
        model = User # the model this form interacts with
        fields = ['username', 'email', 'password1', 'password2']

class DetailsForm(forms.ModelForm):

    class Meta:
        model = Details
        fields = ['role']