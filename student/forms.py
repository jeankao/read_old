# -*- coding: utf-8 -*-
from django import forms
from teacher.models import Classroom
from student.models import Enroll, EnrollGroup, SWork, SFWork

class EnrollForm(forms.Form):
        password =  forms.CharField()
        seat = forms.CharField()
        
        def __init__(self, *args, **kwargs):
            super(EnrollForm, self).__init__(*args, **kwargs)
            self.fields['password'].label = "選課密碼"
            self.fields['seat'].label = "座號"
        
class GroupForm(forms.ModelForm):
        class Meta:
           model = EnrollGroup
           fields = ['name']
           
        def __init__(self, *args, **kwargs):
            super(GroupForm, self).__init__(*args, **kwargs)
            self.fields['name'].label = "組別名稱"

# 組別人數
class GroupSizeForm(forms.ModelForm):
        class Meta:
           model = Classroom
           fields = ['group_size']
        
        def __init__(self, *args, **kwargs):
            super(GroupSizeForm, self).__init__(*args, **kwargs)
            self.fields['group_size'].label = "小組人數"
            
class SeatForm(forms.ModelForm):
        class Meta:
            model = Enroll
            fields = ['seat']
          
class SubmitForm(forms.ModelForm):
        class Meta:
           model = SWork
           fields = ['youtube','memo']
      
        def __init__(self, *args, **kwargs):
            super(SubmitForm, self).__init__(*args, **kwargs)
            self.fields['youtube'].label = "影片網址"
            self.fields['memo'].label = "心得感想"

class ForumSubmitForm(forms.ModelForm):
        class Meta:
           model = SFWork
           fields = ['memo']
      
        def __init__(self, *args, **kwargs):
            super(ForumSubmitForm, self).__init__(*args, **kwargs)
            self.fields['memo'].label = "心得感想"
