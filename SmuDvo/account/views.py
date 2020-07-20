from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm, UserEditForm, \
    ProfileEditForm, EmailPostForm, NewsForm, ConferenceForm, AdsForm
from django.contrib.auth.decorators import login_required, permission_required
from .models import Profile, News, Conference, Ads, Poll
from django.contrib import messages
from django.core.mail import EmailMessage
from .forms import CreatePollForm
from django.shortcuts import redirect
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from .forms import NewsForm, ImagesForm
from .models import Images

from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
import datetime
from django.db.models import Q
from django.views.generic import ListView


from .models import Post, PostImage

def blog_view(request):
    posts = Post.objects.all()
    return render(request, 'blog.html', {'posts':posts})

def detail_view(request, id):
    post = get_object_or_404(Post, id=id)
    photos = PostImage.objects.filter(post=post)
    return render(request, 'detail.html', {
        'post':post,
        'photos':photos
    })




############################ Голосование ###########################

def delete(request, poll_id):
    try:
        poll = Poll.objects.get(id=poll_id)
        poll.delete()
        return home(request)
    except Poll.DoesNotExist:
        return home(request)


def home(request):
    polls = Poll.objects.all()

    context = {
        'polls': polls
    }
    return render(request, 'poll/home.html', context)


def create(request):
    if request.method == 'POST':
        form = CreatePollForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('home')
    else:
        form = CreatePollForm()

    context = {'form': form}
    return render(request, 'poll/create.html', context)


def results(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)

    context = {
        'poll': poll
    }
    return render(request, 'poll/results.html', context)


def vote(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)

    if request.method == 'POST':

        selected_option = request.POST['poll']
        if selected_option == 'option1':
            poll.option_one_count += 1
        elif selected_option == 'option2':
            poll.option_two_count += 1
        elif selected_option == 'option3':
            poll.option_three_count += 1
        else:
            return HttpResponse(400, 'Invalid form option')

        poll.save()

        return redirect('results', poll.id)

    context = {
        'poll': poll
    }
    return render(request, 'poll/vote.html', context)


# from django.core.mail import EmailMessage
# from django.conf import settings


############################## Аккаунт ##############################
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponse('Аутентификация прошла успешно')
            else:
                return HttpResponse('Неверный аккаунт')
        else:
            return HttpResponse('Неверный логин')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'account/register.html',
                  {'user_form': user_form})


def submit_an_application(request):
    user = request.user.profile
    profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
    # user = Profile.objects.get(id=id)
    if not user.user_submit:
        user.user_submit = True
    user.save()
    return HttpResponseRedirect("/account")


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Профиль успешно отредактирован')
        else:
            messages.error(request, 'Ошибка при редактировании профиля')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,
                  'account/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})


############################## Новости ##############################
@permission_required('account.can_add')
def create_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        images = ImagesForm(request.POST, request.FILES,
                               queryset=Images.objects.none())
        if form.is_valid() and images.is_valid():
            form.save()
            images.save()
            return HttpResponseRedirect('/account')
    else:
        form = NewsForm()
        images = ImagesForm()
    return render(request, 'news/create_news.html', {'form': form, 'images': images})


@permission_required('account.can_edit')
def edit_news(request, id):
    n = News.objects.get(id=id)
    news = get_object_or_404(News, id=id)
    images = Images.objects.filter(news=news)
    if request.method == "POST":
        form = NewsForm(data=request.POST, files=request.FILES, instance=n)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/account")
    else:
        form = NewsForm(instance=n)
    return render(request, "news/edit_news.html", {"form": form, 'images':images})



@permission_required('account.can_delete')
def delete_news(request, id):
    new = News.objects.get(id=id)
    new.delete()
    return HttpResponseRedirect("/account")


def list_of_news(request):
    news = News.objects.all()
    return render(request, "news/list_of_news.html", {"news": news})




############################## Объявления ##############################
@permission_required('account.can_add')
def create_ads(request):
    if request.method == 'POST':
        form = AdsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/account')
    else:
        form = NewsForm()
    return render(request, 'ads/create_ads.html', {'form': form})


@permission_required('account.can_edit')
def edit_ads(request, id):
    n = Ads.objects.get(id=id)
    if request.method == "POST":
        form = AdsForm(data=request.POST, files=request.FILES, instance=n)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/account")
    else:
        form = AdsForm(instance=n)
    return render(request, "ads/edit_ads.html", {"form": form})


@permission_required('account.can_delete')
def delete_ads(request, id):
    new = Ads.objects.get(id=id)
    new.delete()
    return HttpResponseRedirect("/account")


def list_of_ads(request):
    ads = Ads.objects.all()
    return render(request, "ads/list_of_ads.html", {"ads": ads})


############################## Конференции ##############################
@permission_required('account.can_add')
def create_conference(request):
    if request.method == "POST":
        conference = ConferenceForm(request.POST)
        conference.save()
        return HttpResponseRedirect("/account")
    else:
        form = ConferenceForm()
        return render(request, "conference/create_conference.html", {"Form": form})


@permission_required('account.can_edit')
def edit_conference(request, id):
    conference = Conference.objects.get(id=id)
    if request.method == "POST":
        conference = ConferenceForm(request.POST, instance=conference)
        conference.save()
        return HttpResponseRedirect("/account")
    else:
        form = ConferenceForm(instance=conference)
        return render(request, "conference/edit_conference.html", {"Form": form})


@permission_required('account.can_delete')
def delete_conference(request, id):
    conference = Conference.objects.get(id=id)
    conference.delete()
    return HttpResponseRedirect("/account")


def list_of_conference(request):
    conference = Conference.objects.all()
    return render(request, "conference/list_of_conference.html", {"conference": conference})


############################## Список пользователей ##############################
@permission_required('account.can_view')
def list_of_scientists(request):
    users = Profile.objects.all()
    return render(request, "scientists/list_of_scientists.html", {"users": users})


@permission_required('account.can_delete')
def delete_user(request, id):
    user = Profile.objects.get(id=id)
    user.user.delete()
    return HttpResponseRedirect("/account")


############################## Список ученых ##############################
@permission_required('account.can_edit')
def add_to_scientists(request, id):  ##добавление в совет
    user = Profile.objects.get(id=id)
    user.scientist = True
    # user.user_is_reject = False
    user.save()
    return HttpResponseRedirect("/account")


@permission_required('account.can_edit')
def delete_from_scientists(request, id):  ##удаление из совета
    user = Profile.objects.get(id=id)
    if not user.user_is_reject and user.scientist:
        user.scientist = False
        user.user_is_reject = False
    elif not user.user_is_reject:
        user.user_is_reject = True
        user.user_submit = False
    user.save()
    return HttpResponseRedirect("/account")


############################## Рассылка ##############################
@permission_required('account.can_edit')
def post_email(request):
    send_mail('Тестик', 'МОЁ СООБЩЕНИЕ', 'salushkin1998@bk.ru', ['kotovamasha6767@mail.ru'],
              fail_silently=False)
    # if request.method == 'POST':
    #     form = EmailPostForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         subject = form.cleaned_data['title']
    #         sender = settings.EMAIL_HOST_USER
    #         recipients = ['lashkevich.pk@gmail.com']
    #         message = form.cleaned_data['text']
    #         if request.FILES:
    #             uploaded_file = request.FILES['file']
    #         try:
    #             email = EmailMessage(subject, message, sender, recipients)
    #             email.attach(uploaded_file.name, uploaded_file.read(), uploaded_file.content_type)
    #             email.send()
    #             messages.success(request, 'Письмо успешно отправлено')
    #             return render(request, 'account/dashboard.html')
    #         except:
    #             return "Ошибка"
    # else:
    #     form = EmailPostForm()
    # return render(request, 'email/email.html', {'form': form})

# @permission_required('account.can_edit')
# def submit_an_application(request, id ):
#     user = Profile.objects.get(id=id)
#     if not user.user_submit:
#         user.user_submit = True
