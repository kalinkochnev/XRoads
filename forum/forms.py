from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, HTML

from accounts.models import CustomUser
from forum.models import Post, SubForum


# NOTE if there is a database query in a form, create tests for migration with the model it queries
# NOTE if migration errors happen as a result of form, move the query to the __init__ someway

class TestAjaxForm(forms.Form):
    action = forms.CharField(max_length=25)

    def clean_action(self):
        action = self.cleaned_data.get('action')
        if action is not None:
            return action
        else:
            raise forms.ValidationError('Action is not valid')

    def complete_action(self, *args, **kwargs):
        do_action = True
        if not do_action:
            return None

        return 'Action was done'


class VotePostForm(forms.Form):
    action = forms.CharField(max_length=25)
    post_id = forms.IntegerField()

    def clean_action(self):
        action = self.cleaned_data.get('action')
        if action not in ['upvote', 'downvote', 'clearvote']:
            raise forms.ValidationError('Not a valid action')
        else:
            return action

    def clean_post_id(self):
        postid = self.cleaned_data.get('post_id')
        if postid is None:
            raise forms.ValidationError('Not a valid action')

        try:
            post = Post.objects.get(id=postid)
        except Post.DoesNotExist:
            raise forms.ValidationError('Post id does not exist')

        return postid


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'attached_file']

    subforum = forms.CharField(widget=forms.Select())

    # TODO clean the file field and make sure it is an image
    def create_post(self, user_obj):
        data = self.cleaned_data

        title = data.get('title')
        body = data.get('text')
        file = data.get('file')
        subforum = data.get('subforum')

        for forum in SubForum.objects.all():
            if str(forum) == subforum:
                subforum = forum

        new_post = Post(
            sub_forum=subforum,
            user=user_obj,
            title=title,
            text=body,
            attached_file=file,
        )
        new_post.save()


class AccountSettingsForm(forms.ModelForm):
    pass
