from django.shortcuts import render
from django.http import HttpResponse
from account.models import *


def index(request):
    conference = Conference.objects.all()
    news = News.objects.all()
    users = Profile.objects.all()
    ads = Ads.objects.all()
    poll = Poll.objects.all()
    return render(request, "index.html", {"users": users, "news": news, "conference": conference, "ads": ads, "polls": poll})