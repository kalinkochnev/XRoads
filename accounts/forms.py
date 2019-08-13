from django.contrib import messages
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
        self.helper.layout = Layout(
            HTML("""<h1 class="h3 mb-3 font-weight-normal">Signup</h1>"""),
            Field('email', placeholder='Email address', css_class='form-control', id='top-field'),
            Field('alias', placeholder='Username', css_class='form-control'),
            Field('password', placeholder='Password', css_class='form-control'),
            Field('confirm_pass', placeholder='Confirm password', css_class='form-control', id='bottom-field'),
            Submit('Sign up', 'Submit', css_class='btn btn-lg btn-primary btn-block', style="margin-top: 20px;")
        )

    email = forms.EmailField()
    alias = forms.CharField(max_length=15)
    password = forms.CharField(max_length=128, widget=forms.PasswordInput)
    confirm_pass = forms.CharField(max_length=128, widget=forms.PasswordInput)

    def signup_user(self, request, *args, **kwargs):
        User = get_user_model()

        if self.fields_correct():
            cd = self.cleaned_data
            email = cd.get('email')
            alias = cd.get('alias')
            password = cd.get('password')

            return User.objects.signup(email, alias, password)

        elif self.pwd_match():
            messages.warning(request, 'Passwords do not match! Please try again.')
        else:
            messages.error(request, 'Incorrect data was entered. Please try again.')

        return None

    # used to verify if the passwords match in to form field
    def pwd_match(self):
        if self.is_valid():
            # cleaned data is the form data that django makes sure is valid so it can be used safely
            cd = self.cleaned_data
            if cd.get('password') == cd.get('confirm_pass'):
                return True
            else:
                return False

    def fields_correct(self):
        if self.pwd_match() and self.is_valid():
            return True
        return False


class LoginForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-signin'
        self.helper.form_method = 'POST'
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            HTML("""<h1 class="h3 mb-3 font-weight-normal">Log In</h1>"""),
            Field('email', placeholder='Email address', css_class='form-control', id='top-field'),
            Field('password', placeholder='Password', css_class='form-control', id='bottom-field'),
            Submit('Submit', 'Login', css_class='btn btn-lg btn-primary btn-block', style="margin-top: 20px;")
        )

    email = forms.EmailField()
    password = forms.CharField(max_length=128, widget=forms.PasswordInput)

    def login_user(self, request):
        User = get_user_model()

        if self.is_valid():
            cd = self.cleaned_data
            email = cd.get('email')
            password = cd.get('password')

            return User.objects.login(email, password)
        else:
            messages.warning(request, 'Incorrect data was entered into a field. Please try again.')
