from django.db import models
from accounts.models import CustomUser
from django.urls import reverse


# TODO rename class to Forum instead of SubForum
class SubForum(models.Model):
    # TODO Add alphanumeric validator
    name = models.CharField(max_length=20, db_column='name')
    description = models.CharField(max_length=500)
    url_name = models.CharField(max_length=25, default="", blank=True)

    # TODO add admins and owner/creator group permission
    __original_name = None

    def __init__(self, *args, **kwargs):
        super(SubForum, self).__init__(*args, **kwargs)
        self.__original_name = self.name

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        if self.name != self.__original_name or not self.url_name:
            self.url_name = self.name.replace(' ', '').lower()
            self.__original_name = self.name
        super(SubForum, self).save(force_insert, force_update, *args, **kwargs)

    def __str__(self):
        return self.name


class SchoolClass(models.Model):
    name = models.CharField(max_length=50)
    grade = models.IntegerField()
    placement = models.CharField(max_length=10)

    teacher = models.ForeignKey(CustomUser, on_delete=models.PROTECT, blank=True)
    students = models.ManyToManyField(CustomUser, related_name="class_students", blank=True)

    def __str__(self):
        return f"{self.name} {self.placement}"


class Post(models.Model):
    school_class = models.ForeignKey(SchoolClass, on_delete=models.SET_NULL, null=True, related_name="post_schoolclass")
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=150)
    text = models.TextField(max_length=20000)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    upvotes = models.ManyToManyField(CustomUser, blank=True, related_name='post_upvotes')
    downvotes = models.ManyToManyField(CustomUser, blank=True, related_name='post_downvotes')

    def is_upvoted(self, user):
        post = Post.objects.get(id=self.id)
        if post.upvotes.filter(id=user.id).exists():
            return True
        return False

    def is_downvoted(self, user):
        post = Post.objects.get(id=self.id)
        if post.downvotes.filter(id=user.id).exists():
            return True
        return False

    @property
    def upvote_count(self):
        return self.upvotes.all().count()

    @property
    def downvote_count(self):
        return self.downvotes.all().count()

    def upvote(self, user):
        post = Post.objects.get(id=self.id)
        if self.is_downvoted(user):
            post.downvotes.remove(user)
        if not self.is_upvoted(user):
            post.upvotes.add(user)

    def downvote(self, user):
        post = Post.objects.get(id=self.id)
        if self.is_upvoted(user):
            post.upvotes.remove(user)
            self.upvote_html_classes = ""
        if not self.is_downvoted(user):
            post.downvotes.add(user)
            self.downvote_html_classes = "selected"

    def clearvote(self, user):
        post = Post.objects.get(id=self.id)
        if self.is_upvoted(user):
            post.upvotes.remove(user)
            self.upvote_html_classes = ""
        if self.is_downvoted(user):
            post.downvotes.remove(user)
            self.downvote_html_classes = ""

    @property
    def get_absolute_url(self):
        return reverse('forumsapp:post', kwargs={'post_id': self.id})


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    text = models.CharField(max_length=1000)
