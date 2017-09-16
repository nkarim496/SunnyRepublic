"""SunnyRepublic URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static
from sunny import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^settings/change_pic/$', views.change_picture, name='change_picture'),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^student_home/$', views.student_home, name='student_home'),
    url(r'^student_lessons/$', views.student_lessons, name='student_lessons'),
    url(r'^student_lessons_ajax/$', views.student_lessons_ajax, name='student_lessons_ajax'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
