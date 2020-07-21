from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings

urlpatterns = [
# posts
    path('blog/', views.blog_view, name='blog'),
    path('<int:id>/', views.detail_view, name='detail'),
    path('list', views.list, name='news'),
    path('detail_news/<int:news_id>/', views.detail_news, name='news_datail'),
    path('detail_news/<int:news_id>/leave_img/', views.leave_img, name='leave_img'),

    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.dashboard, name='dashboard'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('register/', views.register, name='register'),
    path('edit', views.edit, name='edit'),
    path('submit_an_application', views.submit_an_application, name='submit_an_application'),
    path('create_news/', views.create_news, name='create_news'),
    path('list_of_news', views.list_of_news, name='list_of_news'),
    path('delete_news/<int:id>/', views.delete_news),
    path('edit_news/<int:id>', views.edit_news),



# голосование
    path('vote/', views.home, name='home'),
    path('vote/create/', views.create, name='create'),
    path('vote/results/<poll_id>/', views.results, name='results'),
    path('vote/vote/<poll_id>/', views.vote, name='vote'),
    path('vote/delete/<poll_id>/', views.delete, name='delete'),
# голосование

# реализовать
    path('create_ads/', views.create_ads, name='create_ads'),
    path('list_of_ads', views.list_of_ads, name='list_of_ads'),
    path('delete_ads/<int:id>/', views.delete_ads),
    path('edit_ads/<int:id>', views.edit_ads),
# реализовать

    path('list_of_scientists', views.list_of_scientists, name='list_of_scientists'),
    path('delete_user/<int:id>/', views.delete_user),
    path('create_conference/', views.create_conference, name='create_conference'),
    path('list_of_conference', views.list_of_conference, name='list_of_conference'),
    path('delete_conference/<int:id>/', views.delete_conference),
    path('edit_conference/<int:id>', views.edit_conference),
    path('post_email', views.post_email, name='post_email'),
    path('add_to_scientists/<int:id>', views.add_to_scientists, name='add_to_scientists'),
    path('delete_from_scientists/<int:id>', views.delete_from_scientists, name='delete_from_scientists')
]
