from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.views.generic import FormView, TemplateView, ListView, DetailView, UpdateView
import json

from django.views.generic.base import View

from forum.forms import CreatePostForm, VotePostForm
from forum.models import SubForum, Post, Comment


class MultiAjaxHandler:
    handler_dict = {}
    request = None

    def ajax_handler(self, request, *args, **kwargs):
        self.request = request

        if request.POST is not None:
            Form = self.action_router()
            Form = Form(request.POST)

            return self.form_processing(Form, *args, **kwargs)

    def action_router(self):
        if self.request_is_valid():
            data = self.request.POST
            Form = self.handler_dict[data.get('action')]
            return Form
        else:
            return None

    def request_is_valid(self):
        action = self.request.POST.get('action')
        if self.request.is_ajax() and action in self.handler_dict.keys():
            return True
        elif self.request.is_ajax() or action not in self.handler_dict.keys():
            return False

    def form_processing(self, form, *args, **kwargs):
        if form is None:
            return JsonResponse({'status': 'Error. Form blank'})

        if form.is_valid():
            cd = form.cleaned_data
            self.complete_action(*args, **cd, **kwargs)
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse(form.errors, status=400)

    def complete_action(self, *args, **kwargs):
        pass


class AjaxResponseMixin(object):
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """

    def form_invalid(self, form):
        response = super(AjaxResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super(AjaxResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            data = {
                'message': 'Successfully received',
            }
            return JsonResponse(data)
        else:
            return response


# B4COMMIT add login required to cbv
class HomeView(ListView):
    template_name = "forum/home.html"
    queryset = SubForum.objects.all()
    context_object_name = 'forum_list'


class ListPosts(MultiAjaxHandler, ListView):
    template_name = 'forum/forum.html'
    model = Post
    handler_dict = {
        'upvote': VotePostForm,
        'downvote': VotePostForm,
        'clearvote': VotePostForm,
    }

    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        forum_name = self.kwargs['forum_name']
        query = Post.objects.filter(sub_forum__url_name=forum_name)
        return query

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        forum_name = self.kwargs['forum_name']
        context['subforum'] = SubForum.objects.get(url_name=forum_name)
        return context

    def complete_action(self, *args, **kwargs):
        action = kwargs.pop('action')
        post_id = kwargs.pop('post_id')
        user = kwargs.pop('user')
        post = Post.objects.get(id=post_id)

        if action == 'upvote':
            post.upvote(user)
        elif action == 'downvote':
            post.downvote(user)
        elif action == 'clearvote':
            post.clearvote(user)

    def post(self, request, *args, **kwargs):
        return self.ajax_handler(request=request, user=request.user, *args, **kwargs)


class PostDetails(AjaxResponseMixin, DetailView):
    template_name = 'forum/post.html'
    model = Post
    pk_url_kwarg = 'post_id'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        postid = self.kwargs['post_id']
        context['comments_list'] = Comment.objects.filter(post=postid)
        return context


"""
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
            Comment.objects.filter(id=commentid).update(up_votes=(uv + 1))
            post = request.POST.get('post')
            return redirect('/post/?id=' + post)
        elif 'dv-comment' in request.POST:
            commentid = request.POST.get('dv-comment')
            comment = Comment.objects.filter(id=commentid)
            dv = comment.get(id=commentid).down_votes
            Comment.objects.filter(id=commentid).update(down_votes=(dv + 1))
            post = request.POST.get('post')
            return redirect('/post/?id=' + post)
    else:
        return redirect('home')
"""


class CreatePostView(AjaxResponseMixin, FormView):
    form_class = CreatePostForm
    template_name = 'forum/create_post.html'
    success_url = reverse_lazy('forumsapp:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['forum_list'] = [str(subforum) for subforum in SubForum.objects.all()]
        return context

    def form_valid(self, form):
        user = self.request.user
        form.create_post(user_obj=user)
        messages.success(self.request, 'Your post was published')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Your post could not be published. Please try again')
        return HttpResponseRedirect(reverse('create_post'))


def terms_of_service(request):
    return render(request, 'forum/tos.html')


def privacy_policy(request):
    return render(request, 'forum/pp.html')
