# -*- coding: UTF-8 -*-
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views.generic import ListView, CreateView
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import Group
from student.models import Enroll
from teacher.models import Classroom
from account.models import Visitor, VisitorLog
from forms import LoginForm, UserRegistrationForm, PasswordForm, RealnameForm
from django.utils.timezone import localtime
from datetime import datetime
from django.utils import timezone
# 網站首頁
def homepage(request):
    return render_to_response('homepage.html', context_instance=RequestContext(request))

# 網站大廳
def dashboard(request):
        return render_to_response('account/dashboard.html', context_instance=RequestContext(request))
# 使用者登入功能
def user_login(request):
                message = None
                test = ""
                if request.method == "POST":
                                form = LoginForm(request.POST)
                                if form.is_valid():
                                                username = request.POST['username']
                                                password = request.POST['password']
                                                user = authenticate(username=username, password=password)
                                                if user is not None:
                                                                if user.is_active:
                                                                                if user.id == 1:
                                                                                        if user.first_name == "":
                                                                                                user.first_name = "管理員"
                                                                                                user.save()
                                                                                # 登入成功，導到大廳
                                                                                login(request, user)
                                                                                year = localtime(timezone.now()).year
                                                                                month =  localtime(timezone.now()).month
                                                                                day =  localtime(timezone.now()).day
                                                                                date_number = year * 10000 + month*100 + day
                                                                                try:
                                                                                    visitor = Visitor.objects.get(date=date_number)
                                                                                except ObjectDoesNotExist:
                                                                                    visitor = Visitor(date=date_number)
                                                                                visitor.count = visitor.count + 1
                                                                                visitor.save()

                                                                                visitorlog = VisitorLog(visitor_id=visitor.id, user_id=user.id, IP=request.META.get('REMOTE_ADDR'))
                                                                                visitorlog.save()

                                                                                return redirect('/account/dashboard')
                                                                else:
                                                                                message = "帳號未啟用!"
                                                else:
                                                        message = "無效的帳號或密碼!"
                else:
                                form = LoginForm()
                return render_to_response('registration/login.html', {'test': test, 'message': message, 'form': form}, context_instance=RequestContext(request))

# 註冊帳號
def register(request):
        if request.method == 'POST':
                form = UserRegistrationForm(request.POST)
                if form.is_valid():
                        # Create a new user object but avoid saving it yet
                        new_user = form.save(commit=False)
                        # Set the chosen password
                        new_user.set_password(form.cleaned_data['password'])
                        # Save the User object
                        new_user.save()
                        return render_to_response('registration/register_done.html',{'new_user': new_user}, context_instance=RequestContext(request))
        else:
                form = UserRegistrationForm()
        return render_to_response('registration/register.html', {'form': form}, context_instance=RequestContext(request))

# 超級管理員可以查看所有帳號
class UserListView(ListView):
    context_object_name = 'users'
    paginate_by = 20
    template_name = 'account/userlist.html'
    
    def get_queryset(self):      
        if self.request.GET.get('account') != None:
            keyword = self.request.GET.get('account')
            queryset = User.objects.filter(Q(username__icontains=keyword) | Q(first_name__icontains=keyword)).order_by('-id')
        else :
            queryset = User.objects.all().order_by('-id')				
        return queryset

def make(request, action, user_id):
    user = User.objects.get(id=user_id)           
    try :
        group = Group.objects.get(name="teacher")	
    except ObjectDoesNotExist :
        group = Group(name="teacher")
        group.save()
    if action == "1":            
        group.user_set.add(user)
    else : 
        group.user_set.remove(user)  
    return redirect("/account/userlist")        

# 修改密碼
def password(request, user_id):
    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid():
            user = User.objects.get(id=user_id)
            user.set_password(request.POST['password'])
            user.save()             
            return redirect('dashboard')
    else:
        form = PasswordForm()
        user = User.objects.get(id=user_id)

    return render_to_response('form.html',{'form': form, 'user':user}, context_instance=RequestContext(request))
  
# 修改他人的真實姓名
def adminrealname(request, user_id):
    if request.method == 'POST':
        form = RealnameForm(request.POST)
        if form.is_valid():
            user = User.objects.get(id=user_id)
            user.first_name =form.cleaned_data['first_name']
            user.save()              
            return redirect('/account/userlist/')
    else:
        teacher = False
        enrolls = Enroll.objects.filter(student_id=user_id)
        for enroll in enrolls:
            classroom = Classroom.objects.get(id=enroll.classroom_id)
            if request.user.id == classroom.teacher_id:
                teacher = True
                break
        if teacher:
            user = User.objects.get(id=user_id)
            form = RealnameForm(instance=user)
        else:
            return redirect("/")

    return render_to_response('form.html',{'form': form}, context_instance=RequestContext(request))
	
# 修改自己的真實姓名
def realname(request):
    if request.method == 'POST':
        form = RealnameForm(request.POST)
        if form.is_valid():
            user = User.objects.get(id=request.user.id)
            user.first_name =form.cleaned_data['first_name']
            user.save()               
            return redirect('/account/profile/'+str(request.user.id))
    else:
        user = User.objects.get(id=request.user.id)
        form = RealnameForm(instance=user)

    return render_to_response('form.html',{'form': form}, context_instance=RequestContext(request))

# 修改學校名稱
def adminschool(request):
    if request.method == 'POST':
        form = SchoolForm(request.POST)
        if form.is_valid():
            user = User.objects.get(id=request.user.id)
            user.last_name =form.cleaned_data['last_name']
            user.save()
            # 記錄系統事件
            if is_event_open(request) :               
                log = Log(user_id=request.user.id, event=u'修改學校名稱<'+user.last_name+'>')
                log.save()                
            return redirect('/account/profile/'+str(request.user.id))
    else:
        user = User.objects.get(id=request.user.id)
        form = SchoolForm(instance=user)

    return render_to_response('account/school.html',{'form': form}, context_instance=RequestContext(request))
    
# 修改信箱
def adminemail(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            user = User.objects.get(id=user_id)
            user.email =form.cleaned_data['email']
            user.save()
            # 記錄系統事件
            if is_event_open(request) :               
                log = Log(user_id=request.user.id, event=u'修改信箱<'+user.first_name+'>')
                log.save()                
            return redirect('/account/profile/'+str(request.user.id))
    else:
        user = User.objects.get(id=request.user.id)
        form = EmailForm(instance=user)

    return render_to_response('account/email.html',{'form': form}, context_instance=RequestContext(request))    