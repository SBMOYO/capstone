from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('home', views.index, name='index'),
    path('user_registration', views.user_registration, name='user_registration'),
    path('user_login', views.user_login_view, name='user_login'),
    path('user_logout', views.user_logout_view, name='user_logout'),
    path('house_registration', views.house_registration, name='house_registration'),
    path('house/<int:id>', views.house, name='house'),
    path('edit_house/<int:id>', views.edit_house, name='edit_house'),
    path('rent_house/<int:id>', views.rent_house, name='rent_house'),
]