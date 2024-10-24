"""
URL configuration for review_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, re_path
from rating.views import main_view, rate_view, success_view, ReviewListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_view, name='main-view'),
    re_path(r'^(?P<prefilled_order_id>\d{6})/rate/$', rate_view, name='rate-view'),
    path('rate/', rate_view, name='rate-view'),
    path('success/', success_view, name='success-view'),
    path('api/v1/reviews/', ReviewListView.as_view(), name='review-list'),
    re_path(r'^(?P<prefilled_order_id>\d{6})/$', main_view, name='main-view'),
]
