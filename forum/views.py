from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core import serializers
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


"""class MultiAjaxHandler:
    handler_dict = {}
    request = None
    on_success = JsonResponse({'status': 'success'})
    on_failure = JsonResponse({'status': 'error'})

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

    # TODO add tests
    def get_data(self):
        Form = self.action_router()
        if Form.is_valid() and self.request_is_valid():
            return Form.cleaned_data

    def form_processing(self, form, *args, **kwargs):
        if form is None:
            return self.on_failure

        if form.is_valid():
            cd = form.cleaned_data
            self.complete_action(*args, **cd, **kwargs)
            return self.on_success
        else:
            return self.on_failure

    def complete_action(self, *args, **kwargs):
        pass"""

"""class AjaxResponseMixin(object):

    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)


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
            return response"""


class QuerySchoolClass(View):

    def get(self, request, *args, **kwargs):
        data = request.GET
        school_class_list = SchoolClass.objects.filter(class_grade=data.get('grade')).filter(
            class_placement=data.get('placement'))
        output = serializers.serialize('python', school_class_list, fields="")
        return HttpResponse(output, content_type='application/json')


# B4COMMIT add login required to cbv
class HomeView(ListView):
    template_name = "forum/forum_home.html"
    queryset = Post.objects.all()
    context_object_name = 'post_list'
    handler = {
        'create-post': CreatePostForm
    }

    def complete_action(self, *args, **kwargs):
        Post.objects.create(
            post_school_class=SchoolClass.objects.get(id=kwargs.pop('school_class_id')),
            title=kwargs.pop('title'),
            text=kwargs.pop('text'),
            user=self.request.user,
        )

    def post(self, request, *args, **kwargs):
        self.ajax_handler(request=self.request, *args, **kwargs)


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
                body=message,
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
