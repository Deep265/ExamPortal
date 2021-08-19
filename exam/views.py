from django.shortcuts import render,get_object_or_404,redirect
from django.urls import reverse,reverse_lazy
import time
import datetime
# Http Imports

from django.http import HttpResponse,HttpResponseRedirect
# Time Imports
from django.utils.timezone import utc
from django.contrib.auth.models import User
import datetime

# Form imports

# Model Imports
from django.db.models import F
from authorization.models import student_res
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Exam,ExamAns,Tests,registers
# Class based Views imports
from django.views.generic import TemplateView,ListView,DetailView,CreateView,DeleteView
from django.views.generic.edit import FormMixin
from django.contrib.auth import get_user_model
# Create your views here.

def IndexView(request):
    return render(request,'index.html')

class ExamListView(LoginRequiredMixin,ListView):
    login_url = '/authorize/login/'
    model = Exam
    context_object_name = 'exam'


@login_required(login_url='/authorize/login/')
def ExamCreateView(request):
    if request.method == 'POST':
        question = request.POST.get('question')
        option1 = request.POST.get('option1')
        option2 = request.POST.get('option2')
        option3 = request.POST.get('option3')
        option4 = request.POST.get('option4')
        correct = request.POST.get('correct')
        img1 = request.POST.get('img1')
        img2 = request.POST.get('img2')
        img3 = request.POST.get('img3')
        img4 = request.POST.get('img4')
        img5 = request.POST.get('img5')
        subject = request.POST.get('subject')
        exam_img = Exam(user=request.user,question=question,option1=option1,option2=option2,option3=option3,option4=option4,correct=correct,optionimg1=img1,optionimg2=img2,optionimg3=img3,optionimg4=img4,correctimg=img5,subject=subject)
        exam_img.save()
        return HttpResponseRedirect(reverse('exam:exam_list'))
    return render(request,'exam/exam_form.html')



class ExamDetailView(LoginRequiredMixin,DetailView):
    login_url = '/authorize/login/'
    model = Tests
    context_object_name = 'exam'
    template_name = 'exam/exam_detail.html'


    def post(self, request, pk,*args, **kwargs):
        store = request.POST.get('answer')
        ques = request.POST.get('question')
        test = get_object_or_404(Tests,pk=self.kwargs['pk'])
        exam = get_object_or_404(Exam,pk=test.test_question.pk)
        try:
            examans = ExamAns.objects.filter(user=request.user,question__exact=ques,store__isnull=False,test=test).values_list('id',flat=True)[0]
#       print(examans)
            examans_change = get_object_or_404(ExamAns,pk=examans)
#        print(examans_change)
            examans_change.store = store
            examans_change.save()
            if examans == 0:
                examans = ExamAns(user=request.user, question=exam, store=store,test=test)
                examans.save()
        except:
            examans = ExamAns(user=request.user,question=exam,store=store,test=test)
            examans.save()

        ti = get_object_or_404(Tests,pk=self.kwargs['pk'])
        r = registers.objects.filter(student=self.request.user,test=ti)[0]
        print(r)
        r.test_time = request.POST.get('time')
        r.save()
        return HttpResponseRedirect(reverse('test_list'))


class ExamPage(LoginRequiredMixin,TemplateView):
    login_url = '/authorize/login/'
    template_name = 'exam/exam_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['exam'] = Exam.objects.all()
        return context

class ExamTarget(LoginRequiredMixin,TemplateView):
    login_url = '/authorize/login/'
    template_name = 'exam/exam_target.html'
@login_required(login_url='/authorize/login/')
def question_maths(request):
    test1 = Tests.objects.filter(user=request.user,test_subject='maths').values_list('id',flat=True)
    test1 = test1[len(test1)-1]
    test = get_object_or_404(Tests,pk=test1)
    if request.method == 'POST':
        question = request.POST.get('question')
        option1 = request.POST.get('option1')
        option2 = request.POST.get('option2')
        option3 = request.POST.get('option3')
        option4 = request.POST.get('option4')
        correct = request.POST.get('correct')
        img1 = request.POST.get('img1')
        img2 = request.POST.get('img2')
        img3 = request.POST.get('img3')
        img4 = request.POST.get('img4')
        img5 = request.POST.get('img5')

        exam_img = Exam(user=request.user,question=question,option1=option1,option2=option2,option3=option3,option4=option4,correct=correct,optionimg1=img1,optionimg2=img2,optionimg3=img3,optionimg4=img4,correctimg=img5,subject='maths')
        exam_img.save()
        n = Exam.objects.filter(user=request.user,question=question,subject='maths').values_list('id',flat=True)
        n = n[0]
        exam_test = get_object_or_404(Exam,pk=n)
        test2 = Tests(test_end_time=test.test_end_time,test_name=test.test_name,user=request.user,test_question=get_object_or_404(Exam,pk=n),test_subject='maths',test_date=test.test_date,test_time=test.test_time,test_approve=True)
        test2.save()
    return render(request,'test/question_maths.html',context={'sub':'Maths'})
@login_required(login_url='/authorize/login/')
def NewMathsTest(request):
    questions = Exam.objects.filter(subject='maths')
    if request.method == "POST":
        text_name = request.POST['test_name']
        test_date = request.POST['test_date']
        test_time = request.POST['test_time']
        test_end = request.POST['test_end']
        try:
            if request.POST['qu']:
                text_name = request.POST['test_name']
                test_date = request.POST['test_date']
                test_time = request.POST['test_time']
                text_question = request.POST.getlist('qu')
                for i in range(len(text_question)):
                    test = Tests(test_subject='maths',user=request.user,test_end_time=test_end,test_date=test_date,test_time=test_time,test_name=text_name,test_approve=True,test_question=get_object_or_404(Exam,pk=text_question[i]))
                    test.save()
                test = Tests(test_subject='maths',user=request.user,test_end_time=test_end,test_date=test_date,test_time=test_time,test_name=text_name)
                test.save()
                r = registers(student=request.user,time="59:00",test=test)
                r.save()
        except:

            test = Tests(user=request.user,test_end_time=test_end,test_date=test_date,test_time=test_time,test_name=text_name,test_subject='maths')
            test.save()
        return HttpResponseRedirect(reverse('exam:maths_question'))

    return render(request,'test/test_maths.html',context={'questions':questions})
@login_required(login_url='/authorize/login/')
def question_chemistry(request):
    test1 = Tests.objects.filter(user=request.user,test_subject='chemistry').values_list('id',flat=True)
    test1 = test1[len(test1)-1]
    test = get_object_or_404(Tests,pk=test1)
    if request.method == 'POST':
        question = request.POST.get('question')
        option1 = request.POST.get('option1')
        option2 = request.POST.get('option2')
        option3 = request.POST.get('option3')
        option4 = request.POST.get('option4')
        correct = request.POST.get('correct')
        img1 = request.POST.get('img1')
        img2 = request.POST.get('img2')
        img3 = request.POST.get('img3')
        img4 = request.POST.get('img4')
        img5 = request.POST.get('img5')

        exam_img = Exam(user=request.user,question=question,option1=option1,option2=option2,option3=option3,option4=option4,correct=correct,optionimg1=img1,optionimg2=img2,optionimg3=img3,optionimg4=img4,correctimg=img5,subject='chemistry')
        exam_img.save()
        n = Exam.objects.filter(user=request.user,question=question,subject='chemistry').values_list('id',flat=True)
        print(n)
        n = n[0]
        exam_test = get_object_or_404(Exam,pk=n)
        test2 = Tests(test_name=test.test_name,user=request.user,test_question=get_object_or_404(Exam,pk=n),test_subject='chemistry',test_date=test.test_date,test_time=test.test_time,test_approve=True,test_end_time=test.test_end_time)
        test2.save()
    return render(request,'test/question_maths.html',context={'sub':'Chemistry'})
@login_required(login_url='/authorize/login/')
def NewChemistryTest(request):
    questions = Exam.objects.filter(subject='chemistry')
    if request.method == "POST":
        text_name = request.POST['test_name']
        test_date = request.POST['test_date']
        test_time = request.POST['test_time']
        test_end = request.POST['test_end']
        try:
            if request.POST['qu']:
                text_name = request.POST['test_name']
                test_date = request.POST['test_date']
                test_time = request.POST['test_time']
                text_question = request.POST.getlist('qu')
                for i in range(len(text_question)):
                    test = Tests(user=request.user, test_end_time=test_end, test_date=test_date, test_time=test_time,
                                 test_name=text_name, test_approve=True,
                                 test_question=get_object_or_404(Exam, pk=text_question[i]),test_subject='chemistry')
                    test.save()
                test = Tests(test_subject='chemistry', user=request.user, test_end_time=test_end, test_date=test_date,
                             test_time=test_time, test_name=text_name)
                test.save()
                r = registers(student=request.user, time="59:00", test=test)
                r.save()
        except:

            test = Tests(user=request.user, test_end_time=test_end, test_date=test_date, test_time=test_time,
                         test_name=text_name, test_subject='chemistry')
            test.save()
        return HttpResponseRedirect(reverse('exam:chemistry_question'))
    return render(request,'test/test_chemistry.html',context={'questions':questions})
@login_required(login_url='/authorize/login/')
def question_physics(request):
    test1 = Tests.objects.filter(user=request.user,test_subject='physics').values_list('id',flat=True)
    test1 = test1[len(test1)-1]
    test = get_object_or_404(Tests,pk=test1)
    if request.method == 'POST':
        question = request.POST.get('question')
        option1 = request.POST.get('option1')
        option2 = request.POST.get('option2')
        option3 = request.POST.get('option3')
        option4 = request.POST.get('option4')
        correct = request.POST.get('correct')
        img1 = request.POST.get('img1')
        img2 = request.POST.get('img2')
        img3 = request.POST.get('img3')
        img4 = request.POST.get('img4')
        img5 = request.POST.get('img5')

        exam_img = Exam(user=request.user,question=question,option1=option1,option2=option2,option3=option3,option4=option4,correct=correct,optionimg1=img1,optionimg2=img2,optionimg3=img3,optionimg4=img4,correctimg=img5,subject='physics')
        exam_img.save()
        n = Exam.objects.filter(user=request.user,question=question,subject='physics').values_list('id',flat=True)
        n = n[0]
        exam_test = get_object_or_404(Exam,pk=n)
        test2 = Tests(test_end_time=test.test_end_time,test_name=test.test_name,user=request.user,test_question=get_object_or_404(Exam,pk=n),test_subject='physics',test_date=test.test_date,test_time=test.test_time,test_approve=True)
        test2.save()
    return render(request,'test/question_maths.html',context={'sub':'Physics'})
@login_required(login_url='/authorize/login/')
def NewPhysicsTest(request):
    questions = Exam.objects.filter(subject='physics')
    if request.method == "POST":
        text_name = request.POST['test_name']
        test_date = request.POST['test_date']
        test_time = request.POST['test_time']
        test_end = request.POST['test_end']
        try:
            if request.POST['qu']:
                text_name = request.POST['test_name']
                test_date = request.POST['test_date']
                test_time = request.POST['test_time']
                text_question = request.POST.getlist('qu')
                for i in range(len(text_question)):
                    test = Tests(user=request.user, test_end_time=test_end, test_date=test_date, test_time=test_time,
                                 test_name=text_name, test_approve=True,
                                 test_question=get_object_or_404(Exam, pk=text_question[i]),test_subject='physics')
                    test.save()
                test = Tests(test_subject='physics', user=request.user, test_end_time=test_end, test_date=test_date,
                             test_time=test_time, test_name=text_name)
                test.save()
                r = registers(student=request.user, time="59:00", test=test)
                r.save()
        except:

            test = Tests(user=request.user, test_end_time=test_end, test_date=test_date, test_time=test_time,
                         test_name=text_name, test_subject='physics')
            test.save()
        return HttpResponseRedirect(reverse('exam:physics_question'))

    return render(request,'test/test_physics.html',context={'questions':questions})

class TestListView(LoginRequiredMixin,ListView):
    login_url = '/authorize/login/'
    model = Tests
    context_object_name= 'test'
    template_name = 'test/test_list.html'

    def get_queryset(self):
        return Tests.objects.filter(user=self.request.user,test_question=None)

@login_required(login_url='/authorize/login/')
def Endtest(request,pk):
    test = get_object_or_404(Tests,pk=pk)
    test_null = Tests.objects.filter(test_name=test.test_name,test_approve=False,test_question=None)
    r = registers.objects.filter(test=test_null,student=request.user)[0]
    r.end_test = True
    return HttpResponseRedirect(reverse('exam:test_list'))

class TestDetailView(LoginRequiredMixin,DetailView):
    login_url = '/authorize/login/'
    model = Tests
    context_object_name = 'test'
    template_name = 'test/test_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        test = get_object_or_404(Tests,pk=self.kwargs['pk'])
        questions = Tests.objects.filter(test_name=test.test_name,test_approve=True)
        test_null = Tests.objects.filter(test_name=test.test_name, test_approve=False, test_question=None)[0]
        questions_id = list(questions.values_list('id',flat=True))
        all_questions = Tests.objects.filter(test_name=test.test_name,test_approve=True)
        global a
        # a is used to for the next button and passed as a pk in post method for reverse
        try:
            a = questions_id.index(self.kwargs['pk'])
        except:
            a = 0

        context['questions'] = questions[a]

        if a == len(questions_id)-1:
            context['end_link'] = 'Yes'
        else:
            context['end_link'] = None
            a = questions_id[a+1]

        if (datetime.datetime.now().strftime("%H:%M:%S") >= datetime.time(hour=int(test.test_time[0:2]),minute=int(test.test_time[3:5]),second=0).strftime("%H:%M:%S")) and ((datetime.date.today()) == test.test_date):
            context['start'] = 0

        if (datetime.datetime.now().strftime("%H:%M:%S") <= datetime.time(hour=int(test.test_end_time[0:2]),minute=int(test.test_end_time[3:5]),second=0).strftime("%H:%M:%S")) and ((datetime.date.today()) == test.test_date):
            context['end'] = 0



        r = registers.objects.filter(test=test_null,student=self.request.user)[0]
        context['time_remain_min'] = r.time[0:2]
        context['time_remain_sec'] = r.time[3:]



        context['all_questions'] = all_questions
        return context

    def post(self,request,*args,**kwargs):
        test_1 = get_object_or_404(Tests,pk=self.kwargs['pk'])
        store = request.POST.get('answer')
        test_null = Tests.objects.filter(test_name=test_1.test_name,test_approve=False,test_question=None)[0]
        questions_all = Tests.objects.filter(test_name=test_1.test_name,test_approve=True).values_list('id',flat=True)

        if test_null.pk == self.kwargs['pk']:
            test_1 = get_object_or_404(Tests,pk=questions_all[0])
            e = get_object_or_404(Exam,pk=test_1.test_question.pk)
            try:
                examans = \
                ExamAns.objects.filter(user=request.user, question=e, store__isnull=False, test=test_1).values_list(
                    'id', flat=True)[0]
                ans = get_object_or_404(ExamAns, pk=examans)
                ans.store = store
                ans.save()
            except:
                examans = ExamAns(test=test_1, user=request.user, question=e, store=store)
                examans.save()
        else:
            e = get_object_or_404(Exam, pk=test_1.test_question.pk)
            try:
                examans = \
                ExamAns.objects.filter(user=request.user, question=e, store__isnull=False, test=test_1).values_list(
                    'id', flat=True)[0]
                ans = get_object_or_404(ExamAns, pk=examans)
                ans.store = store
                ans.save()
            except:
                examans = ExamAns(test=test_1, user=request.user, question=e, store=store)
                examans.save()

        t = request.POST.get('sup')
        try:
            r = registers.objects.filter(student=self.request.user,test=test_null)[0]
            r.time = t
            r.save()
        except:
            pass

        if a == len(questions_all)-1:
            r = registers.objects.filter(test=test_null, student=self.request.user)[0]
            r.end_test = True
            r.save()
            return HttpResponseRedirect(reverse('exam:test_list'))


        return HttpResponseRedirect(reverse('exam:test_detail',kwargs={'pk':a,'slug':None}))
@login_required(login_url='/authorize/login/')
def TestQuestionDelete(request,pk):
    test = get_object_or_404(Tests, pk=pk)
    if request.method == "POST":

        test.test_approve = False
        test.save()
        return redirect('exam:test_list')
    return render(request,'test/test_question_remove.html',context={'test':test.test_question.question})

class TestDeleteView(LoginRequiredMixin,DeleteView):
    login_url = '/authorize/login/'
    model = Tests
    template_name = 'test/test_delete.html'
    success_url = reverse_lazy('exam:test_list')


def TestIndex(request):
    return render(request,'test/index_test.html')
@login_required(login_url='/authorize/login/')
def AllQuestions(request):
    questions = Exam.objects.all()
    return render(request,'test/all_question.html',context={'question':questions})
@login_required(login_url='/authorize/login/')
def NewTest(request):
    math = Exam.objects.filter(subject='maths').count()
    chemistry = Exam.objects.filter(subject='chemistry').count()
    physics = Exam.objects.filter(subject='physics').count()
    return render(request,'test/test.html',{'math':math,'chemistry':chemistry,'physics':physics})
@login_required(login_url='/authorize/login/')
def add_new_question_detail(request,pk):
    test = get_object_or_404(Tests,pk=pk)
    if request.method == 'POST':
        question = request.POST.get('question')
        option1 = request.POST.get('option1')
        option2 = request.POST.get('option2')
        option3 = request.POST.get('option3')
        option4 = request.POST.get('option4')
        correct = request.POST.get('correct')
        img1 = request.POST.get('img1')
        img2 = request.POST.get('img2')
        img3 = request.POST.get('img3')
        img4 = request.POST.get('img4')
        img5 = request.POST.get('img5')

        exam_img = Exam(user=request.user, question=question, option1=option1, option2=option2, option3=option3,
                        option4=option4, correct=correct, optionimg1=img1, optionimg2=img2, optionimg3=img3,
                        optionimg4=img4, correctimg=img5, subject=test.test_subject)
        exam_img.save()
        n = Exam.objects.filter(user=request.user, question=question, subject=test.test_subject).values_list('id', flat=True)
        n = n[0]
        test1 = Tests(test_name=test.test_name,test_end_time=test.test_end_time,user=request.user,test_time=test.test_time,test_date=test.test_date,test_approve=True,test_question=get_object_or_404(Exam,pk=n),test_subject=test.test_subject)
        test1.save()

    return render(request,'test/question_detail.html',context={'sub':test.test_subject})

@login_required(login_url='/authorize/login/')
def register(request,pk):
    test = get_object_or_404(Tests,pk=pk)
    student = get_object_or_404(User,pk=request.user.id)
    r = registers(test=test,student=student,time=59)
    r.save()
    return HttpResponseRedirect(reverse('exam:test_list'))

@login_required(login_url='/authorize/login/')
def register_list(request):
    r = registers.objects.filter(student=request.user)
    return render(request,'exam/student_register.html',context={'tests':r})

# Not Required Function anymore
@login_required(login_url='/authorize/login/')
def add_all_11th(request,pk):
    student = student_res.objects.filter(std='11th')
    for i in range(len(student)):
        r = registers(test=get_object_or_404(Tests,pk=pk),student=get_object_or_404(User,pk=student[i].user.pk))
        r.save()
    return HttpResponseRedirect(reverse('exam:test_list'))