from django.shortcuts import render

# Create your views here.
def email_confirm_success(request):
    return render(request, 'email_success.html')