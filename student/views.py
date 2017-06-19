# -*- coding: UTF-8 -*-
from django.shortcuts import render
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.views.generic import ListView, CreateView
from student.models import Enroll
from teacher.models import Classroom
from account.models import VisitorLog
from student.forms import EnrollForm, GroupForm, SeatForm, GroupSizeForm

# 列出選修的班級
class ClassroomListView(ListView):
    model = Enroll
    context_object_name = 'enrolls'
    template_name = 'student/classroom.html'
    
    def get_queryset(self):
        queryset = Enroll.objects.filter(student_id=self.request.user.id).order_by("-id")            
        return queryset
    
# 查看可加入的班級
def classroom_add(request):
        classrooms = Classroom.objects.all().order_by('-id')
        classroom_teachers = []
        for classroom in classrooms:
            enroll = Enroll.objects.filter(student_id=request.user.id, classroom_id=classroom.id)
            if enroll.exists():
                classroom_teachers.append([classroom,classroom.teacher.first_name,1])
            else:
                classroom_teachers.append([classroom,classroom.teacher.first_name,0])   
        return render_to_response('student/classroom_add.html', {'classroom_teachers':classroom_teachers}, context_instance=RequestContext(request))
    
# 加入班級
def classroom_enroll(request, classroom_id):
        scores = []
        if request.method == 'POST':
                form = EnrollForm(request.POST)
                if form.is_valid():
                    try:
                        classroom = Classroom.objects.get(id=classroom_id)
                        if classroom.password == form.cleaned_data['password']:
                                enroll = Enroll(classroom_id=classroom_id, student_id=request.user.id, seat=form.cleaned_data['seat'])
                                enroll.save()                                
                        else:
                                return render_to_response('message.html', {'message':"選課密碼錯誤"}, context_instance=RequestContext(request))
                      
                    except Classroom.DoesNotExist:
                        pass
                    
                    
                    return redirect("/student/classroom/")
        else:
            form = EnrollForm()
        return render_to_response('student/classroom_enroll.html', {'form':form}, context_instance=RequestContext(request))
        
# 修改座號
def seat_edit(request, enroll_id, classroom_id):
    enroll = Enroll.objects.get(id=enroll_id)
    if request.method == 'POST':
        form = SeatForm(request.POST)
        if form.is_valid():
            enroll.seat =form.cleaned_data['seat']
            enroll.save()
            classroom_name = Classroom.objects.get(id=classroom_id).name
            return redirect('/student/classroom')
    else:
        form = SeatForm(instance=enroll)

    return render_to_response('form.html',{'form': form}, context_instance=RequestContext(request))  



# 查看班級學生
def classmate(request, classroom_id):
        enrolls = Enroll.objects.filter(classroom_id=classroom_id).order_by("seat")
        enroll_group = []
        classroom_name=Classroom.objects.get(id=classroom_id).name
        for enroll in enrolls:
            login_times = len(VisitorLog.objects.filter(user_id=enroll.student_id))
            enroll_group.append([enroll, login_times])
        return render_to_response('student/classmate.html', {'classroom_name':classroom_name, 'enrolls':enroll_group}, context_instance=RequestContext(request))

# 登入記錄
class LoginLogListView(ListView):
    context_object_name = 'visitorlogs'
    paginate_by = 20
    template_name = 'student/login_log.html'
    def get_queryset(self):
        visitorlogs = VisitorLog.objects.filter(user_id=self.kwargs['user_id']).order_by("-id")         
        return visitorlogs
        
    def get_context_data(self, **kwargs):
        context = super(LoginLogListView, self).get_context_data(**kwargs)
        if self.request.GET.get('page') :
            context['page'] = int(self.request.GET.get('page')) * 20 - 20
        else :
            context['page'] = 0
        return context        
        
