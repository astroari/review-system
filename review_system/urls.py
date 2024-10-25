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
from django.urls import path, re_path, include
from rating.views import main_view, rate_view, success_view, ReviewListView
from django.conf.urls import handler400, handler404
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.views.i18n import JavaScriptCatalog

# Non-localized URLs
urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('api/v1/reviews/', ReviewListView.as_view(), name='review-list'),
    
]

# Localized URLs
localized_urlpatterns = [
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    re_path(r'^(?P<prefilled_order_id>\d{6})/rate/(?P<prefilled_phonenumber>\d{12})/$', rate_view, name='rate-view-prefilled'),
    re_path(r'^(?P<prefilled_order_id>\d{6})/(?P<prefilled_phonenumber>\d{12})/$', main_view, name='main-view-prefilled'),
    path('rate/', rate_view, name='rate-view'),
    path('success/', success_view, name='success-view'),
    path('', main_view, name='main-view'),
]

urlpatterns += i18n_patterns(*localized_urlpatterns)

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        path('rosetta/', include('rosetta.urls')),
    ]
