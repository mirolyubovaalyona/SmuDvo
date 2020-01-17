from django.contrib import admin
from .models import Profile, News, Conference


admin.site.register(News)
admin.site.register(Conference)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'photo', 'organization', 'position', 'bio']
