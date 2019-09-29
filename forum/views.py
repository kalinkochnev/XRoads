from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.db.models import Count
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.views.generic import FormView, TemplateView, ListView, DetailView, UpdateView
import json
from django.core.serializers.python import Serializer

from django.views.generic.base import View
from django.views.generic.edit import FormMixin, BaseFormView

from forum.forms import CreatePostForm, VotePostForm, GetSchoolTopics
from forum.models import SubForum, Post, Comment, SchoolClass
from datetime import datetime, timedelta


def xroads_home(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('forumsapp:home'))
    return render(request, 'forum/xroads_home.html')


"""The router method is to be called on a post request along with any additional arguments to store and be used in 
later methods. The router checks if the request is None and runs the on_fail() method if it is. The request is 
validated depending if ajax is enforced and if it is a post request, on_fail() is run if it is invalid. It then gets 
the appropriate form to use depending on the the route dict values. If it couldn't get a form, on_fail() is run. 
The form gets validated and form_valid is run if successful and form invalid is run which calls on_fail() by default. 
If the form is valid, the form.do_action() method is called on the form class, this does not check if that method 
exists on the form class so make sure you include it. If any exceptions occur with the form.do_action() they will be caught and on_fail() is run"""


class FormRouter:
    request = None
    route_dict = {}
    form = None
    enforce_ajax = False
    form_data = None
    args = None
    kwargs = None

    def get_possible_exceptions(self):
        action = self.get_post_data().get('action')
        return self.route_dict.get(action).get('action_exceptions')

    def set_route_dict(self, dictionary):
        self.route_dict = dictionary

    def set_request(self, request):
        self.request = request

    def get_post_data(self):
        return self.request.POST

    def load_form_data(self):
        if self.form is not None:
            if self.form.is_valid():
                self.form_data = self.form.cleaned_data
                return True
        return False

    def validate_request(self):
        if self.enforce_ajax:
            if self.request.is_ajax():
                return True
            else:
                return False
        else:
            if self.request.method == "POST":
                return True
            else:
                return False

    def setup_dict(self):
        if self.validate_request():
            action = self.get_post_data().get('action')

            if action in self.route_dict.keys():
                return self.route_dict[action].get('form')
        else:
            self.on_fail()

    def update_args(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def route(self, request, *args, **kwargs):
        self.update_args(*args, **kwargs)

        if request is None:
            return self.on_fail()
        else:
            self.request = request

        self.form = self.setup_dict()
        if self.form is not None:
            if self.process_form():
                return self.form_valid()
            else:
                return self.form_invalid()
        else:
            return self.on_fail()

    def process_form(self):
        self.form = self.form(self.request.POST)
        if self.form.is_valid():
            return True
        else:
            return False

    def form_valid(self):
        possible_exceptions = self.get_possible_exceptions()
        try:
            self.form.do_action(self.args, self.kwargs)
        except possible_exceptions:
            return self.on_fail()

        return self.on_success()

    def form_invalid(self):
        self.on_fail()

    def on_success(self):
        return "Success!"

    def on_fail(self):
        return None


class QuerySchoolClass(View):
    data = None

    def get(self, request, *args, **kwargs):
        self.data = request.GET

        if self.validate_grade() and self.validate_placement():
            return self.schoolclass_json_response()
        return JsonResponse({'failure': 'Invalid query'})

    def validate_grade(self):
        if self.data.get('grade') not in ['9', '10', '11', '12']:
            return False
        return True

    def validate_placement(self):
        if self.data.get('subject') not in ['art', 'english', 'language', 'history', 'math', 'music', 'science']:
            return False
        return True

    def schoolclass_json_response(self):
        grade = self.data.get('grade')
        subject = self.data.get('subject')
        school_class_list = SchoolClass.objects.filter(grade=grade).filter(subject=subject)
        output = serializers.serialize('python', school_class_list, fields=('name, placement'))
        for school_class in output:
            school_class.pop('model')

        return JsonResponse(output, safe=False)


class CreatePostView(View):
    http_method_names = ['post']
    post_created = False

    def post(self, request):
        form = CreatePostForm(self.request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            self.create_post(data=cd)

        if self.post_created:
            messages.success(request, "Successfully posted!")
        else:
            messages.error(request, "There was an error while creating your post!")

        return redirect('forumsapp:home')
        # TODO add redirect to post page

    def create_post(self, data):
        title = data.get('title')
        text = data.get('text')
        school_class = data.get('schoolclass_field')

        Post.objects.create(
            school_class_id=school_class,
            user=self.request.user,
            title=title,
            text=text,
        )
        self.post_created = True


# TODO add login required to cbv
class HomeView(ListView):
    template_name = "forum/forum_home.html"
    queryset = Post.objects.order_by('-created_at')
    context_object_name = 'post_list'


class PopularView(ListView):
    template_name = "forum/forum_home.html"
    one_week = datetime.today() - timedelta(days=7)
    queryset = Post.objects.filter(created_at__gt=one_week).annotate(up_count=Count('upvotes')).order_by('-up_count')
    context_object_name = 'post_list'


class GeneralView(ListView):
    template_name = "forum/forum_home.html"
    queryset = Post.objects.filter(school_class__subject="general")


class ListPosts(ListView):
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


class PostDetails(DetailView):
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
        form.create_post(user=user)
        messages.success(self.request, 'Your post was published')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Your post could not be published. Please try again')
        return HttpResponseRedirect(reverse('create_post'))
"""


def terms_of_service(request):
    return render(request, 'forum/tos.html')


def privacy_policy(request):
    return render(request, 'forum/pp.html')
