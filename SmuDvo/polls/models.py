from django.db import models
from account.models import Profile
from django.conf import settings
import datetime


class Question(models.Model):
    poll_title = models.CharField('название опроса', max_length=300)
    date_published = models.DateField(verbose_name="Дата публикации", default=datetime.datetime.now())
    is_active = models.BooleanField(verbose_name="Опубликован")

    def __unicode__(self):
        return self.poll_title

    class Meta:
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'


class Answer(models.Model):
    question_id = models.ForeignKey(Question,  on_delete=models.CASCADE)
    answer = models.TextField('вариант ответа', default='')
    votes = models.IntegerField(verbose_name="Голосов", default=0)

    def __unicode__(self):
        return self.answer

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'


class Voted(models.Model):
    question_id = models.ForeignKey(Question,  on_delete=models.CASCADE)
    profile_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    is_voted = models.BooleanField('проголосовал ли пользователь', default=False)