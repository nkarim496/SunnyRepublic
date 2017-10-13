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
    url(r'^student_books/$', views.student_books, name='student_books'),
    url(r'^student_top/$', views.student_top, name='student_top'),
    url(r'^student_page/(?P<username>[\w_-]+)/$', views.student_page, name='student_page'),
    url(r'^student_search/$', views.student_search, name='student_search'),
    url(r'^get_values_ajax/$', views.get_values_ajax, name='get_values_ajax'),
    url(r'^teacher_home/$', views.teacher_home, name='teacher_home'),
    url(r'^teacher_page/(?P<username>[\w_-]+)/$', views.teacher_page, name='teacher_page'),
    url(r'^lesson/(?P<lesson_id>\d+)/$', views.lesson_page, name='lesson_page'),
    url(r'^lesson/add/$', views.lesson_add, name='lesson_add'),
    url(r'^lesson/edit/(?P<lesson_id>\d+)/$', views.lesson_edit, name='lesson_edit'),
    url(r'^lesson/delete/(?P<lesson_id>\d+)/$', views.lesson_delete, name='lesson_delete'),
    url(r'^value/add/(?P<username>[\w_-]+)/(?P<lesson_id>\d+)/$', views.value_add, name='value_add')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
