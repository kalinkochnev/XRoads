from django import forms

from accounts.models import CustomUser
from forum.models import Post, SubForum, SchoolClass


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

    def do_action(self, *args, **kwargs):
        throw_exception = kwargs.get('throw_exception')
        print(throw_exception)
        if throw_exception:
            raise TypeError
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
        fields = ['title', 'text']

    schoolclass_field = forms.IntegerField()
    subject_input = forms.CharField(max_length=20)
    grade_input = forms.IntegerField()

    def clean_grade(self):
        grade = self.cleaned_data['grade']
        if grade not in [0, 9, 10, 11, 12]:
            raise forms.ValidationError('Not a valid grade')
        else:
            return grade

    def clean_class_field(self):
        class_id = self.cleaned_data['schoolclass_field']
        try:
            SchoolClass.objects.get(id=class_id)
            return class_id
        except SchoolClass.DoesNotExist:
            raise forms.ValidationError('The class does not exist')





"""class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'file']

    class_id = forms.IntegerField()

    # TODO clean the file field and make sure it is an image
    def create_post(self, user_obj):
        data = self.cleaned_data

        title = data.get('title')
        body = data.get('body')
        file = data.get('file')
        class_id = data.get('class_id')

        for assignments in SchoolClass.objects.all():
            if str(assignments) == class_id:
                class_id = assignments

        new_post = Post(
            sub_forum=subforum,
            user=user_obj,
            title=title,
            text=body,
            file=file,
        )
        new_post.save()
"""


class AccountSettingsForm(forms.ModelForm):
    pass


class GetSchoolTopics(forms.Form):
    action = forms.CharField(max_length=25)
    grade = forms.IntegerField()
    placement = forms.CharField(max_length=7)

    def clean_action(self):
        action = self.cleaned_data.get('action')
        if action != 'list_topics':
            raise forms.ValidationError('Not a valid action')
        else:
            return action

    def clean_grade(self):
        grade = self.cleaned_data.get('grade')
        if grade not in range(9, 13):
            raise forms.ValidationError('Not a valid grade')
        else:
            return grade

    def clean_placement(self):
        placement = self.cleaned_data.get('placement')
        if placement not in ['N', 'R', 'H', 'AP']:
            raise forms.ValidationError('Not a valid placement level')
        else:
            return placement
