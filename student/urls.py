# -*- coding: UTF-8 -*-
from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # 選課
    url(r'^classroom/enroll/(?P<classroom_id>[^/]+)/$', views.classroom_enroll),      
    url(r'^classroom/add/$', views.classroom_add),  
    url(r'^classroom/$', views.ClassroomListView.as_view()),
		url(r'^classroom/seat/(?P<enroll_id>\d+)/(?P<classroom_id>\d+)/$', views.seat_edit, name='seat_edit'),
    # 同學
    url(r'^classmate/(?P<classroom_id>\d+)/$', views.classmate), 
    #url(r'^loginlog/(?P<user_id>\d+)/$', views.LoginLogListView.as_view()),    
    #url(r'^calendar/(?P<classroom_id>\d+)/$', views.LoginCalendarClassView.as_view()),     	
]