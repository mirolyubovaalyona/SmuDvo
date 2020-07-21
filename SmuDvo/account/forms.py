
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import *

# Голосование
class CreatePollForm(ModelForm):
    class Meta:
        model = Poll
        fields = ['question', 'option_one', 'option_two', 'option_three']
# Голосование


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_email(self):
        cd = self.cleaned_data
        if len(cd['email']) < 1:
            raise forms.ValidationError('Enter a valid email address.')
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError('This email is already used')
        return cd['email']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        if len(cd['password']) < 6:
            raise forms.ValidationError('Password must be at least 6 simbols')
        num = False
        letr = False
        LETR = False
        for ch in cd['password']:
            if 47 < ord(ch) < 58:
                num = True
            if 64 < ord(ch) < 91:
                LETR = True
            if 96 < ord(ch) < 123:
                letr = True
            if num and letr and LETR:
                return cd['password2']
        raise forms.ValidationError('Password must contain at least one of lower- and upper-case letter and a number')

    def clean_first_name(self):
        cd = self.cleaned_data
        if not (cd['first_name'].isalpha()):
            raise forms.ValidationError('Name must contain only letters')
        return cd['first_name']

    def clean_last_name(self):
        cd = self.cleaned_data
        if not (cd['last_name'].isalpha()):
            raise forms.ValidationError('Name must contain only letters')
        return cd['last_name']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo', 'organization', 'position', 'bio')


class EmailPostForm(forms.Form):
    title = forms.CharField(max_length=50)
    to = forms.EmailField()
    text = forms.CharField(widget=forms.Textarea)
    file = forms.FileField()


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'text']

class NewsFullForm(NewsForm): #extending form
    images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta(NewsForm.Meta):
        fields = NewsForm.Meta.fields + ['images',]

class ImagesForm(forms.ModelForm):
    image = forms.ImageField(label='Image')

    class Meta:
        model = Images
        fields = ('image',)

class AdsForm(forms.ModelForm):
    class Meta:
        model = Ads
        fields = ['title', 'photo', 'text']


class ConferenceForm(forms.ModelForm):
    class Meta:
        model = Conference
        fields = "__all__"
