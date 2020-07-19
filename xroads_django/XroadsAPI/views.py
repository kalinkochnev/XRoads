from django.shortcuts import render


# Create your views here.
def csrf(request):
    return render(request, template_name='home.html')
