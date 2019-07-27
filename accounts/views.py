from django.shortcuts import render
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import redirect


# Create your views here.
def login(request):
    pass


def signup(request):
    User = get_user_model()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if form.pwd_match():
                email = cd.get('email')
                alias = cd.get('alias')
                password = cd.get('password')

                user = User.objects.signup(email, alias, password)
                if user is not None:
                    messages.success(request, 'Your account was created successfully!')
                    return redirect('forums')
                else:
                    messages.error(request, 'The email or password you entered may already be taken')
            else:
                messages.error(request, 'Your passwords do not match')
        else:
            messages.error(request, 'Incorrect data was entered into a field')
    else:
        form = CreateUserForm()
        return render(request, 'signup.html', {'form': form})
    # TODO LATEST ERROR ValueError: The view accounts.views.signup didn't return an HttpResponse object. It returned None instead.


def logout(request):
    pass