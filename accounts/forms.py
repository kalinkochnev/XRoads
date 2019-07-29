from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django import forms


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
class CreateUserForm(forms.ModelForm):
    # meta is used for when you already have a model where you can specify attributes from to use as form fields
    class Meta:
        model = get_user_model()
        fields = ('email', 'alias', 'password')

    # TODO make this password field text hidden
    confirm_pass = forms.CharField(max_length=128)

    # used to verify if the passwords match in to form field
    def pwd_match(self):
        # cleaned data is the form data that django makes sure is valid so it can be used safely
        cd = self.cleaned_data
        if cd.get('password') == cd.get('confirm_pass'):
            return True
        else:
            return False

