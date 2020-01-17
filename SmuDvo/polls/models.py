from django.db import models
from django.conf import settings
import datetime


class Question(models.Model):
    poll_title = models.CharField('название опроса', max_length=300)
    date_published = models.DateField(verbose_name="Дата публикации", default=datetime.datetime.now())
    is_active = models.BooleanField(verbose_name="Опубликован")


class Answer(models.Model):
    question_id = models.ForeignKey(Question, on_dalete=models.CASCADE, on_delete=models.CASCADE)
    answer = models.TextField('вариант ответа', default='')
    votes = models.IntegerField(verbose_name="Голосов", default=0)


class Voted(models.Model):
    question_id = models.ForeignKey(Question, on_dalete=models.CASCADE, on_delete=models.CASCADE)
    is_voted = models.BooleanField('проголосовал ли пользователь', default=False)
