# -*- coding: UTF-8 -*-
from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
        # post views
        url(r'^dashboard/$',  views.dashboard, name='dashboard'),
        #登入
        url(r'^login/$', views.user_login, name='login'),
        #註冊帳號
        url(r'^register/$', views.register, name='register'),
        #登出
        url(r'^logout/$',auth_views.logout),
        #列出所有帳號
        url(r'^userlist/$', views.UserListView.as_view()),
        #設定教師
        url(r'^teacher/make/(?P<action>\d+)/(?P<user_id>\d+)$', views.make), 
        #修改密碼
        url(r'^password-change/$', auth_views.password_change, name='password_change'),
        url(r'^password-change/done/$', auth_views.password_change_done, name='password_change_done'),    
        url(r'^password/(?P<user_id>\d+)/$', views.password),
        #修改真實姓名
        url(r'^realname/(?P<user_id>\d+)/$', views.adminrealname),    
        url(r'^realname/$', views.realname, name='realname'), 
        #修改學校
        url(r'^school/$', views.adminschool),     
        #修改信箱
        url(r'^email/$', views.adminemail),      
]