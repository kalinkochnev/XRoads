from django.shortcuts import render


# Create your views here.
def home(request):
    # get data here from database
    return render(request, 'forum/home.html', {'blah': 123})


def show_forums(request):
    return render(request, 'forum/forum.html')
