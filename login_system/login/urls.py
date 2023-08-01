from django.urls import path
from login.views import *

urlpatterns = [
    path('', User_Login.as_view(),name='user_login'),
    path('user_registration/', User_Registraion.as_view(),name='user_registration'),
]