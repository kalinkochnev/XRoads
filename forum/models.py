from django.db import models
from accounts.models import CustomUser


class SubForum(models.Model):
    name = models.CharField(max_length=25)
    description = models.CharField(max_length=500)
    # TODO add admins and owner/creator

    def __str__(self):
        return self.name


class Post(models.Model):
    sub_forum = models.ForeignKey(SubForum, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    comment = models.ForeignKey('Comment', on_delete=models.SET_NULL, null=True)

    title = models.CharField(max_length=50)
    text = models.TextField(max_length=20000)
    attached_file = models.FileField()
    up_votes = models.IntegerField()
    down_votes = models.IntegerField()


class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)

    text = models.CharField(max_length=1000)
    up_votes = models.IntegerField()
    down_votes = models.IntegerField()