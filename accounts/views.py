from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render
from .forms import SignupForm
from .forms import LoginForm
from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.shortcuts import redirect


@login_required  # TODO: Add Redirect
def view_logout(request):
    logout(request)
    return redirect('home')


def view_login(request):
    if request.method == 'POST' and request.POST:
        # tries to create a new user object, if it is None that means that the user is already taken
        form = LoginForm(request.POST)
        user = form.login_user(request)

        if user is not None:
            login(request, user)

            messages.success(request, 'Login successful! Welcome, ' + str(user))

            # TODO what does this do? Does it redirect to the page if you need to login? Please document
            if request.GET.get('next') is not None:
                return redirect(request.GET.get('next'))
            else:
                return redirect('home')
        else:
            messages.error(request, 'Incorrect username or password! Please try again.')

    return render(request, 'accounts/login.html', {'form': LoginForm()})


def signup(request):
    # gets user model using get_user_model
    User = get_user_model()

    # form submissions are always POST requests so run form processing if it is POST
    if request.method == 'POST' and request.POST:
        # use the imported form that was made in forms.py
        form = SignupForm(request.POST)

        # tries to create a new user object, if it is None that means that the user is already taken
        user = form.signup_user(request)
        if user is not None:
            messages.success(request, 'Your account was created successfully! Welcome, ' + str(user))
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'The email you entered is already in use! Please try again.')

    # if a different request type is made this is run. If there are any errors with the form this also runs
    form = SignupForm()
    return render(request, 'accounts/signup.html', {'form': form, })


@login_required
def account(request):
    return render(request, "accounts/accountsettings.html", {'user': request.user});
