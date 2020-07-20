from django.contrib import admin
from .models import Profile, News, Conference, Images


admin.site.register(Conference)

class ImagesInline(admin.StackedInline):
    model = Images
    extra = 0

class NewsAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,
         {'fields': ['title', 'text']}
         ),
    ]
    inlines = [ImagesInline]

admin.site.register(News, NewsAdmin)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'photo', 'organization', 'position', 'bio']
