from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# TODO create links to other pages for easier basic navigation while making the site
import accounts
from forum.models import SubForum, Post, Comment


from forum.forms import CreatePostForm


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


@login_required()
def show_post(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        post = Post.objects.all().get(id=id)
        comments = Comment.objects.all().filter(post=id)
        return render(request, 'forum/post.html', {'post': post, 'comments': comments})
    elif request.method == 'POST':
        for key in request.POST:
            print(key)
            value = request.POST[key]
            print(value)
        if 'message' in request.POST:
            message = request.POST.get('message')
            post = request.POST.get('post')
            new_comment = Comment(
                post=Post.objects.get(id=post),
                user=request.user,
                text=message,
                up_votes=0,
                down_votes=0
            )
            if message != "":
                new_comment.save()
                return redirect('/post/?id=' + post)
            else:
                messages.warning(request, "The Comment cannot be Blank! Please try again.")
                return redirect('/post/?id=' + post)
        elif 'uv-comment' in request.POST:
            commentid = request.POST.get('uv-comment')
            comment = Comment.objects.filter(id=commentid)
            uv = comment.get(id=commentid).up_votes
            Comment.objects.filter(id=commentid).update(up_votes=(uv+1))
            post = request.POST.get('post')
            return redirect('/post/?id=' + post)
        elif 'dv-comment' in request.POST:
            commentid = request.POST.get('dv-comment')
            comment = Comment.objects.filter(id=commentid)
            dv = comment.get(id=commentid).down_votes
            Comment.objects.filter(id=commentid).update(down_votes=(dv + 1))
            post = request.POST.get('post')
            return redirect('/post/?id=' + post)
        elif 'uv-post' in request.POST:
            postid = request.POST.get('uv-post')
            post = Post.objects.filter(id=postid)
            uv = post.get(id=postid).up_votes
            Post.objects.filter(id=postid).update(up_votes=(uv + 1))
            post = request.POST.get('post')
            return redirect('/post/?id=' + postid)
        elif 'dv-post' in request.POST:
            postid = request.POST.get('dv-post')
            post = Post.objects.filter(id=postid)
            dv = post.get(id=postid).down_votes
            Post.objects.filter(id=postid).update(down_votes=(dv + 1))
            post = request.POST.get('post')
            return redirect('/post/?id=' + postid)
    else:
        return redirect('home')



@login_required()
def create_post(request):
    if request.method == 'POST':
        form = CreatePostForm(request.POST)

        if form.is_valid():
            form.create_post(request.user)
            messages.success(request, 'Your post was published')
        else:
            messages.error(request, 'An incorrect field was entered')
    else:
        form = CreatePostForm()

    return render(request, 'forum/create_post.html', {'form': form})
