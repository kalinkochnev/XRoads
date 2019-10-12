from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django import forms


# NOTE if there is a database query in a form, create tests for migration with the model it queries
# NOTE if migration errors happen as a result of form, move the query to the __init__ someway


# These next two are for the admin page
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = get_user_model()
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ('email',)


# This is the form used for signing up on the signup view
class SignupForm(forms.Form):
    email = forms.EmailField()
    alias = forms.CharField(max_length=15)
    password = forms.CharField(max_length=128, widget=forms.PasswordInput)
    confirm_pass = forms.CharField(max_length=128, widget=forms.PasswordInput)

    def signup_user(self):
        User = get_user_model()
        cd = self.cleaned_data
        return User.objects.signup(email=cd.get('email'), alias=cd.get('alias'), password=cd.get('password'))

    def clean_confirm_pass(self):
        cd = self.cleaned_data
        password = cd.get('confirm_pass')
        if password is None:
            raise forms.ValidationError('You did not confirm your password')
        return password

    def clean_password(self):
        cd = self.cleaned_data
        password = cd.get('password')
        if password is None:
            # TODO create message system that gets first value from form errors and displays it
            raise forms.ValidationError('Password was not entered')
        return password

    def clean_email(self):
        cd = self.cleaned_data
        email = cd.get('email')
        if email is None:
            raise forms.ValidationError('Email was not entered')
        return email

    def clean_alias(self):
        cd = self.cleaned_data
        alias = cd.get('alias')
        if alias is None:
            raise forms.ValidationError('Username was not entered')
        return alias

    def clean(self):
        password = self.clean_password()
        confirm_pass = self.clean_confirm_pass()
        if password != confirm_pass:
            raise forms.ValidationError('Passwords do not match')

    # used to verify if the passwords match in to form field
    def pwd_match(self):
        if self.is_valid():
            # cleaned data is the form data that django makes sure is valid so it can be used safely
            cd = self.cleaned_data

    def fields_correct(self):
        if self.pwd_match() and self.is_valid():
            return True
        return False


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(max_length=128, widget=forms.PasswordInput)

    def clean_email(self):
        cd = self.cleaned_data
        email = cd.get('email')
        if email is None:
            raise forms.ValidationError('A field was blank')
        else:
            return email

    def clean_password(self):
        cd = self.cleaned_data
        password = cd.get('password')
        if password is None:
            raise forms.ValidationError('A field was blank')
        else:
            return password

    def clean(self):
        User = get_user_model()
        email = self.clean_email()
        password = self.clean_password()

        if User.objects.login(email, password) is None:
            raise forms.ValidationError('Incorrect username or password! Please try again')

    def login_user(self):
        User = get_user_model()
        cd = self.cleaned_data
        return User.objects.login(cd['email'], cd['password'])
