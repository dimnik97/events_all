"""events_all URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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


from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

import main_app.views
from profiles.views import JointLoginSignupView
from . import settings


urlpatterns = [
    path('', main_app.views.index, name='index'),
    url(r'^map/$', main_app.views.event_map, name='map'),
    url(r'^friends/$', main_app.views.friends, name='map'),
    path('admin/', admin.site.urls),
    path('main_app/', include('main_app.urls')),
    path('accounts/', include('allauth.urls')),
    path('profile/', include('profiles.urls')),
    path('groups/', include('groups.urls')),
    path('cities/', include('cities_.urls')),
    path('events/', include('events_.urls')),
    path('chats/', include('chats.urls')),
    path('cities_/', include('cities_.urls')),
    url(r'^accounts/signup-or-login/', JointLoginSignupView.as_view(),
        name='signup_or_login'),
    # url(r'^$', RedirectView.as_view(url='/main_app')),
]


urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)