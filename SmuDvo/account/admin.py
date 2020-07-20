from django.contrib import admin
from .models import Profile, News, Conference, Images

from django.contrib import admin

from .models import Post, PostImage

class PostImageAdmin(admin.StackedInline):
    model = PostImage

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [PostImageAdmin]

    class Meta:
       model = Post

@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    pass

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
