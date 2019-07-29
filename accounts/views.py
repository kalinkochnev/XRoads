from django.shortcuts import render
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import redirect


# TODO make login view
def login(request):
    return render(request, 'login.html')


def signup(request):
    # gets user model using get_user_model
    User = get_user_model()

    # form submissions are always POST requests so run form processing if it is POST
    if request.method == 'POST':
        # use the imported form that was made in forms.py
        form = CreateUserForm(request.POST)

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
                    return redirect('login')
                else:
                    messages.error(request, 'The email or password you entered may already be taken')
            else:
                messages.error(request, 'Your passwords do not match')
        else:
            messages.error(request, 'Incorrect data was entered into a field')

    # if a different request type is made this is run. If there are any errors with the form this also runs
    form = CreateUserForm()
    return render(request, 'signup.html', {'form': form})


# TODO make logout view
def logout(request):
    pass