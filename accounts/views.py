from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .forms import SignupForm
from .forms import LoginForm
from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.shortcuts import redirect


@login_required   # TODO: Adding Redirect
def view_logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


def view_login(request):
    # gets user model using get_user_model
    User = get_user_model()

    # form submissions are always POST requests so run form processing if it is POST
    if request.method == 'POST':
        # use the imported form that was made in forms.py
        form = LoginForm(request.POST)

        # django checks that the fields of the form pass criteria based on the field type specified
        if form.is_valid():
            cd = form.cleaned_data

            email = cd.get('email')
            password = cd.get('password')

            # tries to create a new user object, if it is None that means that the user is already taken
            user = User.objects.login(email, password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful!')
                return redirect('home')
            else:
                messages.error(request, 'The username or password you entered was incorrect')
        else:
            messages.warning(request, 'Incorrect data was entered into a field')

    # if a different request type is made this is run. If there are any errors with the form this also runs
    form = LoginForm()
    return render(request, 'login.html', {'form': form, })


def signup(request):
    # gets user model using get_user_model
    User = get_user_model()

    # form submissions are always POST requests so run form processing if it is POST
    if request.method == 'POST':
        # use the imported form that was made in forms.py
        form = SignupForm(request.POST)

        # django checks that the fields of the form pass criteria based on the field type specified
        if form.is_valid():
            cd = form.cleaned_data

            # makes sures the passwords match using method in CreateUserForm
            if form.pwd_match():
                email = cd.get('email')
                alias = cd.get('alias')
                password = cd.get('password')

                # tries to create a new user object, if it is None that means that the user is already taken
                user = User.objects.signup(email, alias, password)
                if user is not None:
                    messages.success(request, 'Your account was created successfully!')
                    login(request, user)
                    return redirect('home')
                else:
                    messages.error(request, 'The email or password you entered may already be taken')
            else:
                messages.warning(request, 'Your passwords do not match')
        else:
            messages.warning(request, 'Incorrect data was entered into a field')

    # if a different request type is made this is run. If there are any errors with the form this also runs
    form = SignupForm()
    return render(request, 'signup.html', {'form': form, })
