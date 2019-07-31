from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, HTML


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

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-signin'
        self.helper.form_method = 'POST'
        self.helper.form_show_labels = False
        self.helper.add_input(
            Submit('Sign up', 'Submit', css_class='btn btn-lg btn-primary btn-block', style="margin-top: 20px;"))
        self.helper.layout = Layout(
            HTML("""<h1 class="h3 mb-3 font-weight-normal">Signup</h1>"""),
            Field('email', placeholder='Email address', css_class='form-control', id='top-field'),
            Field('alias', placeholder='Username', css_class='form-control'),
            Field('password', placeholder='Password', css_class='form-control'),
            Field('confirm_pass', placeholder='Confirm password', css_class='form-control', id='bottom-field'),

        )

    email = forms.EmailField()
    alias = forms.CharField(max_length=15)
    password = forms.CharField(max_length=128, widget=forms.PasswordInput)
    confirm_pass = forms.CharField(max_length=128, widget=forms.PasswordInput)

    # used to verify if the passwords match in to form field
    def pwd_match(self):
        # cleaned data is the form data that django makes sure is valid so it can be used safely
        cd = self.cleaned_data
        if cd.get('password') == cd.get('confirm_pass'):
            return True
        else:
            return False
