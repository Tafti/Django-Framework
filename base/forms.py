from django.forms import ModelForm
from .models import Room
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User





class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'  # or specify fields like ['name', 'description']    




class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['email', 'password1']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize field labels/placeholders
        # self.fields['username'].widget.attrs.update({'placeholder': 'Choose a username'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Enter your email'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Create a password'})
        # self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm password'})
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email        