from django.db import models


# Create your models here.


class QuestionMixin(models.Model):
    class Meta:
        abstract = True

    text = models.CharField(max_length=1000)


class NumberResponse(QuestionMixin):
    response = models.DecimalField(decimal_places=5, max_digits=10)


class TextResponse(QuestionMixin):
    response = models.CharField(max_length=1000)


class MathResponse(QuestionMixin):
    response = models.CharField(max_length=50)


class Quiz(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    questions = models.ManyToManyField(QuestionMixin)
