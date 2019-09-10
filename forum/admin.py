from django.contrib import admin
from .models import SubForum, Post, Comment, SchoolClass
# Register your models here.

admin.site.register(SubForum)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(SchoolClass)
