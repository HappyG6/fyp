from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Contact,Pdf


class CustomUserForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-styling'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-styling'}), required=True)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-styling'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-styling'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ContactForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Your Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Your Email'}))
    subject = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Subject'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','placeholder':'Please write something for us'}))

    class Meta:
        model = Contact
        fields = '__all__'

class PDFForm(forms.ModelForm):
    name = forms.CharField(required=True)
    role = forms.CharField(required=True)
    datestart = forms.CharField(required=True)
    dateend = forms.CharField(required=True)

    class Meta:
        model = Pdf
        fields = '__all__'

