"""msgr URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from messaging.views import RecentConversationsView, SendMessageView, UserMessagesView, updates_view

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^updates/(?P<user_id>[0-9]+)/', updates_view),
    url(r'^api/', include([
        url(r'recent-conversations/', RecentConversationsView.as_view()),
        url(r'send-message/', SendMessageView.as_view()),
        url(r'(?P<from>[0-9]+)/messages/(?P<to>[0-9]+)/', UserMessagesView.as_view()),
    ])),
]
