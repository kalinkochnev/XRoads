from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, HTML
from forum.models import Post, SubForum


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'attached_file']

    def __init__(self, *args, **kwargs):
        super(CreatePostForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = "form-add-post"
        self.helper.form_method = 'POST'
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Field('title', placeholder='Post title'),
            Field('subforum'),
            Field('text', placeholder='Post Body'),
            Field('attached_file', label='Attach a file'),
            Submit('Post', 'Submit'),
        )

    form_choices = [(str(subforum), str(subforum)) for subforum in SubForum.objects.all()]
    print(form_choices)
    subforum = forms.CharField(widget=forms.Select(choices=form_choices))

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
            up_votes=0,
            down_votes=0,
        )
        new_post.save()
