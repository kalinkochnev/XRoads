from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django import forms

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = get_user_model()
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = get_user_model()
        fields = ('email',)


class CreateUserForm(forms.ModelForm):
    
    class Meta:
        model = get_user_model()
        fields = ('email', 'alias', 'password')

    confirm_pass = forms.CharField(max_length=128)

    # TODO get a better name for this
    def pwd_match(self):
        cd = self.cleaned_data
        if cd.get('password') == cd.get('confirm_pass'):
            return True
        else:
            return False
