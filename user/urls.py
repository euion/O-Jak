"""RoomMate_Match_Serve URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from user import views

app_name = 'login'

urlpatterns = [
    # get login/ -> token, redirect index/
    path('login/', views.login, name="login"),
    # get signup/, post signup/ -> redirect login/
    path('signup/', views.signup, name="signup"), 
    path('signup_quest/', views.signup_question, name="signup_question"),   
    path('logout/', views.logout, name="logout"),
    #mypage μμ μΆκ°
    path('mypage/', views.mypage, name="mypage"),
]
