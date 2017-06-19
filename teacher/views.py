# -*- coding: UTF-8 -*-
from django.shortcuts import render
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.views.generic import ListView, DetailView, CreateView
from teacher.models import Classroom, TWork
from student.models import Enroll, EnrollGroup, SWork, Assistant
from .forms import ClassroomForm, WorkForm
from django.core.exceptions import ObjectDoesNotExist

# 判斷是否為授課教師
def is_teacher(user, classroom_id):
    return user.groups.filter(name='teacher').exists() and Classroom.objects.filter(teacher_id=user.id, id=classroom_id).exists()



# 列出所有課程
class ClassroomListView(ListView):
    model = Classroom
    context_object_name = 'classrooms'
    template_name = 'teacher/classroom.html'
    paginate_by = 20
    def get_queryset(self):      
        queryset = Classroom.objects.filter(teacher_id=self.request.user.id).order_by("-id")
        return queryset
        
#新增一個課程
class ClassroomCreateView(CreateView):
    model = Classroom
    form_class = ClassroomForm
    template_name = 'form.html'    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.teacher_id = self.request.user.id
        self.object.save()
        # 將教師設為0號學生
        enroll = Enroll(classroom_id=self.object.id, student_id=self.request.user.id, seat=0)
        enroll.save()            
        return redirect("/teacher/classroom")        
        
# 修改選課密碼
def classroom_edit(request, classroom_id):
    # 限本班任課教師
    if not is_teacher(request.user, classroom_id):
        return redirect("homepage")
    classroom = Classroom.objects.get(id=classroom_id)
    if request.method == 'POST':
        form = ClassroomForm(request.POST)
        if form.is_valid():
            classroom.name =form.cleaned_data['name']
            classroom.password = form.cleaned_data['password']
            classroom.save()
            return redirect('/teacher/classroom')
    else:
        form = ClassroomForm(instance=classroom)

    return render_to_response('form.html',{'form': form}, context_instance=RequestContext(request))        
    
# 退選
def unenroll(request, enroll_id, classroom_id):
    # 限本班任課教師
    if not is_teacher(request.user, classroom_id):
        return redirect("homepage")    
    enroll = Enroll.objects.get(id=enroll_id)
    enroll.delete()
    classroom_name = Classroom.objects.get(id=classroom_id).name
    return redirect('/student/classmate/'+classroom_id)  
  
# 列出所有課程
class WorkListView(ListView):
    model = TWork
    context_object_name = 'works'
    paginate_by = 20
    def get_queryset(self):
        queryset = TWork.objects.filter(teacher_id=self.request.user.id, classroom_id=self.kwargs['classroom_id']).order_by("-id")
        return queryset
			
    def get_context_data(self, **kwargs):
        context = super(WorkListView, self).get_context_data(**kwargs)
        context['classroom_id'] = self.kwargs['classroom_id']
        return context	
        
#新增一個課程
class WorkCreateView(CreateView):
    model = TWork
    form_class = WorkForm
    template_name = "form.html"
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.teacher_id = self.request.user.id
        self.object.classroom_id = self.kwargs['classroom_id']
        self.object.save()  
  
        return redirect("/teacher/work/"+self.kwargs['classroom_id'])        
        
# 修改選課密碼
def work_edit(request, classroom_id):
    # 限本班任課教師
    if not is_teacher(request.user, classroom_id):
        return redirect("homepage")
    classroom = Classroom.objects.get(id=classroom_id)
    if request.method == 'POST':
        form = ClassroomForm(request.POST)
        if form.is_valid():
            classroom.name =form.cleaned_data['name']
            classroom.password = form.cleaned_data['password']
            classroom.save()
                  
            return redirect('/teacher/classroom')
    else:
        form = ClassroomForm(instance=classroom)

    return render_to_response('form.html',{'form': form}, context_instance=RequestContext(request))        
    			
# 列出某作業所有同學名單
def work_class(request, classroom_id, work_id):
    enrolls = Enroll.objects.filter(classroom_id=classroom_id)
    classroom_name = Classroom.objects.get(id=classroom_id).name
    classmate_work = []
    scorer_name = ""
    for enroll in enrolls:
        try:    
            work = SWork.objects.get(student_id=enroll.student_id, index=work_id)
            if work.scorer > 0 :
                scorer = User.objects.get(id=work.scorer)
                scorer_name = scorer.first_name
            else :
                scorer_name = "1"
        except ObjectDoesNotExist:
            work = SWork(index=work_id, student_id=1)
        try:
            group_name = EnrollGroup.objects.get(id=enroll.group).name
        except ObjectDoesNotExist:
            group_name = "沒有組別"
        assistant = Assistant.objects.filter(classroom_id=classroom_id, student_id=enroll.student_id, lesson=work_id)
        if assistant.exists():
            classmate_work.append([enroll,work,1, scorer_name, group_name])
        else :
            classmate_work.append([enroll,work,0, scorer_name, group_name])   
    def getKey(custom):
        return custom[0].seat
	
    classmate_work = sorted(classmate_work, key=getKey)
    
        
    return render_to_response('teacher/twork_class.html',{'classmate_work': classmate_work, 'classroom_id':classroom_id, 'index': work_id}, context_instance=RequestContext(request))
	
	# 教師評分
def scoring(request, classroom_id, user_id, index):
    user = User.objects.get(id=user_id)
    enroll = Enroll.objects.get(classroom_id=classroom_id, student_id=user_id)
    try:
        assistant = Assistant.objects.filter(classroom_id=classroom_id,lesson=index,student_id=request.user.id)
    except ObjectDoesNotExist:            
        if not is_teacher(request.user, classroom_id):
            return render_to_response('message.html', {'message':"您沒有權限"}, context_instance=RequestContext(request))
        
    try:
        work3 = SWork.objects.get(student_id=user_id, index=index)
    except ObjectDoesNotExist:
        work3 = SWork(index=index, student_id=user_id)
        
    if request.method == 'POST':
        form = ScoreForm(request.user, request.POST)
        if form.is_valid():
            work = SWork.objects.filter(index=index, student_id=user_id)
            if not work.exists():
                work = SWork(index=index, student_id=user_id, score=form.cleaned_data['score'], publication_date=timezone.now())
                work.save()
                  
            else:
                if work[0].score < 0 :   
                    # 小老師
                    if not is_teacher(request.user, classroom_id):
    	                # credit
                        update_avatar(request.user.id, 2, 1)
                        # History
                        history = PointHistory(user_id=request.user.id, kind=2, message='1分--小老師:<'+index.encode('utf-8')+'><'+enroll.student.first_name.encode('utf-8')+'>', url=request.get_full_path())
                        history.save()				
    
				    # credit
                    update_avatar(enroll.student_id, 1, 1)
                    # History
                    history = PointHistory(user_id=user_id, kind=1, message='1分--作業受評<'+index.encode('utf-8')+'><'+request.user.first_name.encode('utf-8')+'>', url=request.get_full_path())
                    history.save()		                        
                
                work.update(score=form.cleaned_data['score'])
                work.update(scorer=request.user.id)
                # 記錄系統事件
                if is_event_open(request) :                   
                    log = Log(user_id=request.user.id, event=u'更新評分<'+user.first_name+u'><'+str(work[0].score)+u'分>')
                    log.save()                    
						
            if is_teacher(request.user, classroom_id):         
                if form.cleaned_data['assistant']:
                    try :
					    assistant = Assistant.objects.get(student_id=user_id, classroom_id=classroom_id, lesson=index)
                    except ObjectDoesNotExist:
                        assistant = Assistant(student_id=user_id, classroom_id=classroom_id, lesson=index)
                        assistant.save()	
                        
                    # create Message
                    title = "<" + assistant.student.first_name.encode("utf-8") + u">擔任小老師<".encode("utf-8") + index.encode('utf-8') + ">"
                    url = "/teacher/score_peer/" + str(index) + "/" + classroom_id + "/" + str(enroll.group) 
                    message = Message.create(title=title, url=url, time=timezone.now())
                    message.save()                        
                    
                    group = Enroll.objects.get(classroom_id=classroom_id, student_id=assistant.student_id).group
                    if group > 0 :
                        enrolls = Enroll.objects.filter(group = group)
                        for enroll in enrolls:
                            # message for group member
                            messagepoll = MessagePoll.create(message_id = message.id,reader_id=enroll.student_id)
                            messagepoll.save()
                    
                return redirect('/teacher/work/class/'+classroom_id+'/'+index)
            else: 
                return redirect('/teacher/score_peer/'+index+'/'+classroom_id+'/'+str(enroll.group))

    else:
        work = SWork.objects.filter(index=index, student_id=user_id)
        if not work.exists():
            form = ScoreForm(user=request.user)
        else:
            form = ScoreForm(instance=work[0], user=request.user)
    return render_to_response('teacher/scoring.html', {'form': form,'work':work3, 'student':user, 'classroom_id':classroom_id}, context_instance=RequestContext(request))

# 小老師評分名單
def score_peer(request, index, classroom_id, group):
    try:
        assistant = Assistant.objects.get(lesson=index, classroom_id=classroom_id, student_id=request.user.id)
    except ObjectDoesNotExist:
        return redirect("/student/group/work/"+index+"/"+classroom_id)

    enrolls = Enroll.objects.filter(classroom_id=classroom_id, group=group)
    lesson = ""
    classmate_work = []
    for enroll in enrolls:
        if not enroll.student_id == request.user.id : 
            scorer_name = ""
            try:    
                work = Work.objects.get(user_id=enroll.student.id, index=index)
                if work.scorer > 0 :
                    scorer = User.objects.get(id=work.scorer)
                    scorer_name = scorer.first_name
            except ObjectDoesNotExist:
                work = Work(index=index, user_id=1, number="0")        
            classmate_work.append([enroll.student,work,1, scorer_name])
        lesson = lesson_list[int(index)-1]
   
    return render_to_response('teacher/score_peer.html',{'enrolls':enrolls, 'classmate_work': classmate_work, 'classroom_id':classroom_id, 'lesson':lesson, 'index': index}, context_instance=RequestContext(request))
  