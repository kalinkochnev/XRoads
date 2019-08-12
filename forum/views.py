from django.contrib import messages
from django.shortcuts import render
from forum.models import SubForum, Post
from forum.forms import CreatePostForm


def home(request):
    subforums = SubForum.objects.all()
    return render(request, 'forum/home.html', {'subforums': subforums})


def show_posts(request):
    id = request.POST.get('forumid')
    forum = Post.objects.all().filter(sub_forum=id)
    return render(request, 'forum/forum.html', {'forum': forum})


def show_post(request):
    id = request.POST.get('postid')
    post = Post.objects.all().get(id=id)
    return render(request, 'forum/post.html', {'post': post})


def create_post(request):
    if request.method == 'POST':
        form = CreatePostForm(request.POST)

        if form.is_valid():
            pass

        else:
            messages.warning('Incorrect data was entered into the fields')

    else:
        form = CreatePostForm()

    return render(request, 'forum/create_post.html', {'form': form})
