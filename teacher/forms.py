# -*- coding: utf-8 -*-
from django import forms
from teacher.models import Classroom, TWork
from student.models import SWork

# 新增一個課程表單
class ClassroomForm(forms.ModelForm):
        class Meta:
           model = Classroom
           fields = ['name','password']
        
        def __init__(self, *args, **kwargs):
            super(ClassroomForm, self).__init__(*args, **kwargs)
            self.fields['name'].label = "班級名稱"
            self.fields['password'].label = "選課密碼"

# 新增一個作業
class WorkForm(forms.ModelForm):
        class Meta:
           model = TWork
           fields = ['title']
        
        def __init__(self, *args, **kwargs):
            super(WorkForm, self).__init__(*args, **kwargs)
            self.fields['title'].label = "作業名稱"
            
# 作業評分表單           
class ScoreForm(forms.ModelForm):
        RELEVANCE_CHOICES = (
            (100, "你好棒(100分)"),
            (90, "90分"),
            (80, "80分"),
            (70, "70分"),
            (60, "60分"),
        )
        score = forms.ChoiceField(choices = RELEVANCE_CHOICES, required=True, label="分數")
        #if user.groups.all()[0].name == 'teacher': 
        assistant = forms.BooleanField(required=False,label="小老師")
    
        class Meta:
           model = SWork
           fields = ['score']
		   
        def __init__(self, user, *args, **kwargs): 
            super(ScoreForm, self).__init__(*args, **kwargs)	
            if user.groups.all().count() == 0 :
                del self.fields['assistant']
Check_CHOICES = (
    (100, "你好棒(100分)"),
    (90, "90分"),
    (80, "80分"),
    (70, "70分"),
    (60, "60分"),
    (40, "40分"),
    (20, "20分"),
    (0, "0分"),			
)		