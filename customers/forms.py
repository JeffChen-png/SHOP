from django import forms
from django.contrib.auth.models import User
from .models import Customer


class DoubleAuth(forms.Form):
    code = forms.CharField()


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    # def clean_password(self):
    #     cd = self.cleaned_data
    #     if len(cd['password']) < 6:
    #         raise forms.ValidationError('Password must be longer than 6 characters.')
    #     if cd['password'] != cd['password2']:
    #         raise forms.ValidationError('Passwords don\'t match.')
    #     return cd['password']

    def clean_email(self):
        cd = self.cleaned_data
        for user in User.objects.all():
            if user.email == cd['email']:
                raise forms.ValidationError('Email error.')
        return cd['email']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('date_of_birth', 'photo', 'phone', 'address', 'postal_code', 'city', 'region')
