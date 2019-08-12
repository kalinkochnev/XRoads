from django.shortcuts import render, redirect

# TODO create links to other pages for easier basic navigation while making the site
import accounts
from forum.models import SubForum, Post


def home(request):
    subforums = SubForum.objects.all()
    return render(request, 'forum/home.html', {'subforums': subforums})


def show_posts(request):
    if request.method == 'POST':
        id = request.POST.get('forumid')
        forum = Post.objects.all().filter(sub_forum=id)
        return render(request, 'forum/forum.html', {'forum': forum, 'subforum': SubForum.objects.get(id=id)})
    else:
        return redirect('home')


def show_post(request):
    if request.method == 'POST':
        id = request.POST.get('postid')
        post = Post.objects.all().get(id=id)
        return render(request, 'forum/post.html', {'post': post})
    else:
        return redirect('home')

def view_post(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        post = Post.objects.all().get(id=id)
        return render(request, 'forum/post.html', {'post': post})
