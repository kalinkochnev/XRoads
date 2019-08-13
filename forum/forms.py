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
        self.helper = FormHelper()
        self.helper.form_class = "form-add-post"
        self.helper.form_method = 'POST'
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            HTML("""<h1 class="h3 mb-3 font-weight-normal">Create Post</h1>"""),
            Field('title', placeholder='Post title', css_class='form-control', id='top-field'),
            Field('subforum', css_class='form-control'),
            Field('text', placeholder='Post Body', css_class='form-control'),
            Field('attached_file', label='Attach a file', css_class='form-control', id='bottom-field'),
            Submit('Post', 'Submit', css_class='btn btn-lg btn-primary btn-block', style="margin-top: 20px;"),
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
