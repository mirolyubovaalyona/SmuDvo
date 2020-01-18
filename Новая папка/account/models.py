from django.db import models
from django.conf import settings


# class Add_to():
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m-%d/', blank=True)
    organization = models.CharField(max_length=200, default='')
    position = models.CharField(max_length=200, default='')
    bio = models.TextField(default='')
    scientist = models.NullBooleanField(default=False)
    user_is_reject = models.NullBooleanField(default=False)
    user_submit = models.NullBooleanField(default=False)


class Ads(models.Model):
    title = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='ads/%Y/%m-%d/', blank=True)
    text = models.TextField(default='')


class News(models.Model):
    title = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='news/%Y/%m-%d/', blank=True)
    text = models.TextField(default='')


class Conference(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField(default='')
    date = models.CharField(max_length=100)
    place = models.CharField(max_length=200)
