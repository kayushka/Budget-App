"""project0 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, include, re_path

from noname.views import AddIncome, List, AddExpense, Home, SignUp

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path('home/$', Home.as_view(), name='home'),
    re_path('accounts/', include('django.contrib.auth.urls'), name='login'),
    re_path('add_income/$', AddIncome.as_view()),
    re_path('list/$', List.as_view(), name='list'),
    re_path('add_expense/$', AddExpense.as_view()),
    re_path('signup/$', SignUp.as_view(), name='signup'),
]
