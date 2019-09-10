from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

from accounts import AccountExceptions
from accounts.models import CustomUser
from .forms import SignupForm
from .forms import LoginForm
from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.shortcuts import redirect


@login_required  # TODO: Add Redirect
def view_logout(request):
    logout(request)
    return redirect('forumsapp:home')


class LoginClass(FormView):
    template_name = 'accounts/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('forumsapp:home')

    def form_invalid(self, form):
        messages.error(self.request, 'Incorrect username or password! Please try again')
        return super().form_invalid(form)

    def form_valid(self, form):
        user = form.login_user()
        login(self.request, user)
        messages.success(self.request, f'Login successful! Welcome {str(user)}')
        return super().form_valid(form)


class SignupClass(FormView):
    template_name = 'accounts/signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('forumsapp:home')

    def form_invalid(self, form):
        messages.error(self.request, 'There was a problem with the information you put in. Please try again')
        return super().form_invalid(form)

    def form_valid(self, form):
        user = form.signup_user()
        login(self.request, user)
        messages.success(self.request, f'Signup successful! Welcome {str(user)}')
        return super().form_valid(form)


class AccountView(TemplateView):
    template_name = "accounts/account.html"


@login_required
def account(request):
    return render(request, "accounts/accountsettings.html", {'user': request.user});


@login_required
def chgpass(request):
    if request.method == 'POST':
        if request.user.check_password(request.POST.get('cpass')):
            if request.POST.get('npass') == request.POST.get('cnpass'):
                user = request.user
                messages.success(request, "Password changed for user @" + request.user.alias + "#" + str(
                    request.user.user_tag) + "!")
                user.set_password(request.POST.get('npass'))
                user.save()
            else:
                messages.error(request, "New Password and Confirmation did not match! Please try again.")
        else:
            messages.error(request, "Current Password incorrect! Please try again.")

    return redirect('account')


@login_required
def chgusername(request):
    if request.method == 'POST':
        user = CustomUser.objects.get(id=request.user.id)
        equaluser = CustomUser.objects.filter(alias=request.POST.get('username'), user_tag=user.user_tag).count()
        changetag = False
        if equaluser > 0 and CustomUser.objects.get(alias=request.POST.get('username'),
                                                    user_tag=user.user_tag).id != user.id:
            changetag = True
        user.set_alias(request.POST.get('username'))
        if changetag:
            user.generate_unique_tag()
        messages.success(request, "Username changed successfully!")
    return redirect('account')


@login_required
def chgtag(request):
    if request.method == 'POST':
        user = CustomUser.objects.get(id=request.user.id)
        if 'tag' in request.POST:
            continuesave = True
            noerror = True
            try:
                user.validate_tag(int(request.POST.get('tag')))
                user.set_tag(request.POST.get('tag'))
            except AccountExceptions.OutOfBounds:
                noerror = False
                messages.error(request, "Tag randomized. Provided tag is not 4 digits! Please try again.")
                user.generate_unique_tag()
            except AccountExceptions.NoAvailableTags:
                continuesave = False
                messages.error(request, "No tags are available under this Username! Please try again.")
            except AccountExceptions.TagTaken:
                noerror = False
                messages.error(request, "Tag randomized. Desired tag was taken by another user.")
                user.generate_unique_tag()
            if int(request.POST.get('tag')) < 1000:
                messages.error(request, "Tag randomized. Provided tag is not 4 digits! Please try again.")
                user.generate_unique_tag()
                noerror = False
        if continuesave == True:
            user.save()
            if noerror == True:
                messages.success(request, "Username changed successfully!")

    return redirect('account')
