from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm, UserEditForm, \
    ProfileEditForm, EmailPostForm, NewsForm, ConferenceForm
from django.contrib.auth.decorators import login_required, permission_required
from .models import Profile, News, Conference
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings


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
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/account')
    else:
        form = NewsForm()
    return render(request, 'news/create_news.html', {'form': form})


@permission_required('account.can_edit')
def edit_news(request, id):
    n = News.objects.get(id=id)
    if request.method == "POST":
        form = NewsForm(data=request.POST, files=request.FILES, instance=n)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/account")
    else:
        form = NewsForm(instance=n)
    return render(request, "news/edit_news.html", {"form": form})


@permission_required('account.can_delete')
def delete_news(request, id):
    new = News.objects.get(id=id)
    new.delete()
    return HttpResponseRedirect("/account")


def list_of_news(request):
    news = News.objects.all()
    return render(request, "news/list_of_news.html", {"news": news})


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
    if request.method == 'POST':
        form = EmailPostForm(request.POST, request.FILES)
        if form.is_valid():
            subject = form.cleaned_data['title']
            sender = settings.EMAIL_HOST_USER
            recipients = ['lashkevich.pk@gmail.com']
            message = form.cleaned_data['text']
            if request.FILES:
                uploaded_file = request.FILES['file']
            try:
                email = EmailMessage(subject, message, sender, recipients)
                email.attach(uploaded_file.name, uploaded_file.read(), uploaded_file.content_type)
                email.send()
                messages.success(request, 'Письмо успешно отправлено')
                return render(request, 'account/dashboard.html')
            except:
                return "Ошибка"
    else:
        form = EmailPostForm()
    return render(request, 'email/email.html', {'form': form})


# @permission_required('account.can_edit')
# def submit_an_application(request, id ):
#     user = Profile.objects.get(id=id)
#     if not user.user_submit:
#         user.user_submit = True
