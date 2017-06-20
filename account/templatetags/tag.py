# -*- coding: UTF-8 -*-
from django import template
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import Group 
from teacher.models import Classroom
from django.contrib.auth.models import User

register = template.Library() 

@register.filter(name='has_group') 
def has_group(user, group_name):
    try:
        group =  Group.objects.get(name=group_name) 
    except ObjectDoesNotExist:
        group = None
    return group in user.groups.all()
  
@register.filter()
def teacher_id(classroom_id):
    if classroom_id > 0 :
        teacher_id = Classroom.objects.get(id=classroom_id).teacher_id
        return teacher_id
    else : 
        return 0
      
@register.filter()
def name(user_id):
    if user_id > 0 :
        user = User.objects.get(id=user_id)
        return user.first_name
    else : 
        return "匿名"
      
@register.filter()
def number(youtube):
    number_pos = youtube.find("v=")
    number = youtube[number_pos+2:number_pos+13]
    return number