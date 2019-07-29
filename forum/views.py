from django.shortcuts import render


# TODO create links to other pages for easier basic navigation while making the site
def home(request):
    return render(request, 'forum/home.html', {'blah': 123})


def show_forums(request):
    return render(request, 'forum/forum.html')
