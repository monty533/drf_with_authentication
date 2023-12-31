"""drf_task URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from apis import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register_user', views.RegisterUser.as_view(), name='register'),
    path('user_login', views.UserLogin.as_view(), name='login'),
    path('get_user', views.GetUser.as_view(), name='getuser'),
    path('blogs', views.BlogApis.as_view(), name='blogs'),
    path('articles', views.ArticleApis.as_view(), name='articles')
]
