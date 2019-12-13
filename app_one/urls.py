from django.urls import path
from . import views

# NO LEADING SLASHES
urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('wishes', views.wishes_page, name='wishes_page'),
    path('wishes/new', views.new_wish_page, name='new_wish_page'),
    path('create_wish', views.create_wish, name='create_wish'),
    path('remove/<int:wish_id>', views.remove, name='remove'),
    path('wishes/edit/<int:wish_id>', views.edit_page, name='edit_page'),
    path('update/<int:current_wish_id>', views.edit, name='edit'),
    path('grant_wish/<int:wish_id>', views.grant_wish, name='grant_wish'),
    path('wishes/stats', views.stat_page, name='stat_page'),
    path('like/<int:wish_id>', views.like, name='like'),
]
