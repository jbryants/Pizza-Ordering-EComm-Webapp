from django.urls import path

from .views import register_page, login_page, logout_user

app_name = 'users'

urlpatterns = [
    path('register/', register_page, name='register'),
    path('login/', login_page, name='login'),
    path('logout/', logout_user, name='logout')
]
