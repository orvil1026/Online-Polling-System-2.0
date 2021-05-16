 
from django.contrib.auth import login
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.contrib import messages
import datetime
from .models import Quiz,Poll
from .forms import *

from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.http import JsonResponse

from django.views import View
from .models import *
import random
# Create your views here.
#
@login_required()
def quiz(request):
    quiz_exists=False
    all_quiz_id=Quiz.objects.all()

    if request.method == 'POST':

        form = EnterQuizForm(request.POST)

        if form.is_valid():

            entered_quiz_id = form.cleaned_data['quiz_id']
            try:

                quiz = Quiz.objects.get(quiz_id__exact=entered_quiz_id)

                start = quiz.start_time
                end = quiz.end_time
                now = datetime.datetime.now(start.tzinfo)

                if not start < now < end or not quiz.active:
                    messages.success(request, 'Quiz Currently not active!',
                                     extra_tags='alert alert-warning alert-dismissible fade show')
                else:
                    q_id = quiz.id
                    all_polls = quiz.poll_set.all()
                    messages.success(request,'WELCOME!',
                                    extra_tags='alert alert-success alert-dismissible fade show')
                    context = {
                        'quiz_id': quiz.quiz_id,
                        'all_polls': all_polls,
                        'q_id': q_id
                        }
                    quiz_exists = True
                    return HttpResponseRedirect(reverse('polls:list', args=(q_id,)))
            except ObjectDoesNotExist:
                messages.error(request, 'Registration failed!',
                        extra_tags='alert alert-warning alert-dismissible fade show')
                return redirect('polls:quiz')

    else:
        form=EnterQuizForm()
    return render(request,'polls/quiz_id.html', {'form':form})

#
#
@login_required()
def polls_list(request, quiz_pk):
    quiz = Quiz.objects.get(id__exact=quiz_pk)
    all_polls = quiz.poll_set.all().order_by('id')

    request.session['quizId'] = quiz_pk

    search_term = ''
    if 'name' in request.GET:
        all_polls = all_polls.order_by('text')

    if 'date' in request.GET:
        all_polls = all_polls.order_by('pub_date')

    if 'vote' in request.GET:
        all_polls = all_polls.annotate(Count('vote')).order_by('vote__count')

    if 'search' in request.GET:
        search_term = request.GET['search']
        all_polls = all_polls.filter(text__icontains=search_term)

    paginator = Paginator(all_polls, 6)  # Show 6 contacts per page
    page = request.GET.get('page')
    polls = paginator.get_page(page)

    get_dict_copy = request.GET.copy()
    params = get_dict_copy.pop('page', True) and get_dict_copy.urlencode()
    print(params)
    context = {
        'polls': polls,
        'params': params,
        'search_term': search_term,
        'quiz_pk': quiz_pk
    }
    return render(request, 'polls/polls_list.html', context)

@login_required()
def poll_detail(request, poll_id,quiz_pk, *args, **kwargs):

    poll = get_object_or_404(Poll, id=poll_id)

    # if not poll.active:
    #
    #     return render(request,'polls/poll_result.html',{'poll':poll,'quiz_id':quiz_id})

    loop_count = poll.choice_set.count()
    context = {
        'poll': poll,
        'loop_time': range(0, loop_count),
        'quiz_pk': quiz_pk

    }

    return render(request,'polls/poll_detail.html', context)


@login_required()
def vote_detail(request, poll_id,quiz_pk, *args, **kwargs):

    poll = get_object_or_404(Poll, id=poll_id)


    if not poll.active:

        return render(request,'polls/poll_result.html',{'poll':poll,'quiz_pk':quiz_pk})

    loop_count = poll.choice_set.count()
    context = {
        'poll': poll,
        'loop_time': range(0, loop_count),
        'quiz_pk': quiz_pk

    }

    return render(request, 'polls/vote_detail.html', context)

@login_required()
def poll_vote(request, poll_id, quiz_pk):
    poll = get_object_or_404(Poll, pk=poll_id)
    choice_id = request.POST.get('choice')

    if not poll.user_can_vote(request.user):
        messages.error(
            request, "You already voted this poll", extra_tags='alert alert-warning alert-dismissible fade show')
        return redirect("polls:vote-detail", poll_id=poll.id, quiz_pk=quiz_pk)

    if choice_id:
        choice = Choice.objects.get(id=choice_id)
        student = Student.objects.filter(user=request.user).first()
        vote = Vote(user=request.user, poll=poll, choice=choice, student=student)
        vote.save()
        print(vote)
        return redirect("polls:list", quiz_pk=quiz_pk)
    else:
        messages.error(
            request, "No choice selected", extra_tags='alert alert-warning alert-dismissible fade show')
        return redirect("polls:vote-detail", poll_id=poll.id, quiz_pk=quiz_pk)

    return render(request, "polls/poll_result.html", {'poll':poll,'quiz_pk':quiz_pk,'poll_id':poll_id})


@login_required()
def resultsData(request,quiz_pk , poll_id):
    votedata = []
    poll = get_object_or_404(Poll, pk=poll_id)
    votes = poll.choice_set.all()

    for i in votes:
        votedata.append({i.choice_text: i.get_vote_count})
    print(votedata)

    return JsonResponse(votedata, safe=False)


@login_required()
def teacher_resultsData(request, quiz_pk, poll_id):

    poll = get_object_or_404(Poll, pk=poll_id)
    return render(request, "polls/poll_result.html", {'poll': poll, 'quiz_pk': quiz_pk, 'poll_id': poll_id, 'teacher':True})


@login_required
def end_quiz(request, quiz_pk):

    quiz = Quiz.objects.get(id__exact=quiz_pk)

    if quiz.active:

        quiz.active = False
        poll_list = quiz.poll_set.all()

        for poll in poll_list:
            poll.active = False
            poll.save()
        quiz.save()
    else:
        quiz.active = True
        quiz.save()

    return redirect('polls:quiz-detail', quiz_pk=quiz_pk)\

@login_required
def end_poll(request, quiz_pk, poll_id):

    poll = Poll.objects.get(id__exact=poll_id)

    if poll.active:

        poll.active = False
        poll.save()
    else:
        poll.active = True
        poll.save()

    return redirect('polls:quiz-detail', quiz_pk=quiz_pk)

@login_required
def classroom_delete(request, class_pk):
    classroom = get_object_or_404(Classroom, pk=class_pk)
    classroom.delete()
    messages.success(request, "Classroom Deleted successfully",
                     extra_tags='alert alert-success alert-dismissible fade show')
    return redirect("polls:classroom-list")


@login_required
def quiz_delete(request, quiz_pk):
    quiz = get_object_or_404(Quiz, pk=quiz_pk)
    quiz.delete()
    messages.success(request, "Quiz Deleted successfully",
                     extra_tags='alert alert-success alert-dismissible fade show')
    return redirect("polls:quiz-list")


@login_required
def polls_delete(request, poll_id, quiz_pk):
    poll = get_object_or_404(Poll, pk=poll_id)
    poll.delete()
    messages.success(request, "Poll Deleted successfully",
                     extra_tags='alert alert-success alert-dismissible fade show')
    return redirect("polls:quiz-detail", quiz_pk=quiz_pk)


@login_required
def choice_edit(request, choice_id, poll_id, quiz_pk):
    choice = get_object_or_404(Choice, pk=choice_id)
    poll = get_object_or_404(Poll, pk=choice.poll.id)

    if request.method == 'POST':
        form = ChoiceAddForm(request.POST, instance=choice)
        if form.is_valid:
            new_choice = form.save(commit=False)
            new_choice.poll = poll
            new_choice.save()
            messages.success(
                request, "Choice Updated successfully", extra_tags='alert alert-success alert-dismissible fade show')
            return redirect('polls:detail', quiz_pk=quiz_pk, poll_id=poll_id)
    else:
        form = ChoiceAddForm(instance=choice)
    context = {
        'form': form,
        'edit_choice': True,
        'choice': choice,
        'quiz_pk': quiz_pk,
        'poll_id': poll_id
    }
    return render(request, 'polls/add_choice.html', context)

@login_required
def polls_edit(request, poll_id, quiz_pk):
    poll = get_object_or_404(Poll, pk=poll_id)

    if request.method == 'POST':
        form = EditPollForm(request.POST, instance=poll)
        if form.is_valid():
            form.save()
            messages.success(request, "Poll Updated successfully",
                             extra_tags='alert alert-success alert-dismissible fade show')
            return redirect('polls:detail', quiz_pk=quiz_pk, poll_id=poll_id)

    else:
        form = EditPollForm(instance=poll)

        context = {
            'form': form,
            'quiz_pk': quiz_pk,
            'poll_id': poll_id
        }

        return render(request,'polls/poll_edit.html',context)



    return redirect('polls:detail',quiz_pk=quiz_pk,poll_id=poll_id)



@login_required()
def polls_add(request, quiz_pk, *args, **kwargs):

    if request.method == 'POST':
        form = PollAddForm(request.POST)

        if form.is_valid:
            quiz = Quiz.objects.get(id__exact=quiz_pk)
            poll = form.save(commit=False)
            poll.quiz = quiz

            poll.save()
            new_choice1 = Choice(
                poll=poll, choice_text=form.cleaned_data['choice1']).save()
            new_choice2 = Choice(
                poll=poll, choice_text=form.cleaned_data['choice2']).save()
            new_choice3 = Choice(
                poll=poll, choice_text=form.cleaned_data['choice3']).save()
            new_choice4 = Choice(
                poll=poll, choice_text=form.cleaned_data['choice4']).save()

            messages.success(
                request, "Poll & Choices added successfully",
                extra_tags='alert alert-success alert-dismissible fade show')

            return redirect('polls:quiz-detail', quiz_pk=quiz_pk)
    else:
        form = PollAddForm()
    context = {
        'form': form,
        'quiz_pk': quiz_pk
    }
    return render(request, 'polls/add_poll.html', context)


class ClassroomCreateView(View):

    template_name = 'teacher/create_classroom.html'

    def generate_quiz_id(self):

        n = 6
        id = ''
        lower_case = "qwertyuiopasdfghjklzxcvnm"
        upper_case = 'QWERTYUIOPASDFGHKJKLZXCVBNM'
        numbers = '1234567890'

        all = lower_case + upper_case + numbers

        for i in range(6):
            id += all[random.randint(0, len(all)-1)]

        return id

    def get(self, request):
        initial_data = {
            'class_id': str(self.generate_quiz_id())
        }
        form = CreateClassroomForm(initial=initial_data)
        context = {
            'form': form,
        }

        return render(request, self.template_name, context)

    def post(self, request):
        form = CreateClassroomForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            teacher = Teacher.objects.filter(user=request.user).first()
            instance.teacher = teacher
            instance.save()
            form = CreateClassroomForm()

        context = {
            'form': form,
        }
        return redirect('polls:classroom-list')


class TeacherHomeView(View):

    template_name = 'teacher/homepage.html'

    def get(self, request):
        return render(request, self.template_name, {})


class CreateTeacherView(View):

    template_name = 'teacher/create_teacher.html'

    def get(self, request):
        if Teacher.objects.filter(user=request.user):
            return redirect('polls:teacher-homepage')
        else:
            form = CreateTeacherForm()
            context = {
                'form': form
            }
            return render(request, self.template_name, context)

    def post(self, request):
        form = CreateTeacherForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()

        return redirect('polls:teacher-homepage')


class ClassroomListView(View):
    template_name = 'teacher/classroom_list.html'

    def get(self, request):
        teacher = Teacher.objects.filter(user=request.user).first()
        object_list = Classroom.objects.filter(teacher=teacher)
        context = {
            'object_list': object_list,
        }
        return render(request, self.template_name, context)


class StudentHomeView(View):

    template_name = 'student/homepage.html'

    def get(self, request):
        return render(request, self.template_name, {})


class CreateStudentView(View):

    template_name = 'student/create_student.html'

    def get(self, request):
        if Student.objects.filter(user=request.user):
            return redirect('polls:student-homepage')
        else:
            form = CreateStudentForm()
            context = {
                'form': form
            }
            return render(request, self.template_name, context)

    def post(self, request):
        form = CreateStudentForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()

        return redirect('polls:student-homepage')


class EnterClassroomView(View):
    template_name = 'student/join_classroom.html'

    def get(self, request):
        return render(request, self.template_name, {})

    def post(self,request):
        class_id = request.POST.get('class_id')
        classroom_queryset = Classroom.objects.filter(class_id=class_id)

        for class_room in classroom_queryset.iterator():

            if class_room.class_id == class_id:

                classroom = class_room
                student = Student.objects.get(user=request.user)
                is_already_present = StudiesIn.objects.filter(classroom=classroom, student=student)

                if is_already_present.exists():
                    messages.error(request, "Already in Classroom",
                                   extra_tags='alert alert-warning alert-dismissible fade show')
                    return render(request, self.template_name, {})
                else:

                    studies_in = StudiesIn(classroom=classroom, student=student)
                    studies_in.save()
                    messages.error(request, "Successfully Entered Classroom", extra_tags='alert alert-success alert-dismissible fade show')
                    return redirect('polls:student-classroom-list')
            else:
                messages.error(request,"Wrong Classroom Id", extra_tags='alert alert-warning alert-dismissible fade show')
                return render(request, self.template_name, {})


class StudentClassroomListView(View):
    template_name = 'student/classroom_list.html'

    def get(self, request):
        object_list = []
        student = Student.objects.filter(user=request.user).first()
        studies_in = StudiesIn.objects.filter(student=student)

        for item in studies_in:
            object_list.append(item.classroom)

        context = {
            'object_list': object_list,
        }

        return render(request, self.template_name, context)


class CreateQuizView(View):
    template_name = 'teacher/create_quiz.html'

    def get(self, request):
        form = CreateQuizForm()
        context = {
            'form': form,
            'update': False
        }

        return render(request, self.template_name, context)

    def post(self, request):
        form = CreateQuizForm(request.POST)
        if form.is_valid():
            quiz_id = form.cleaned_data['quiz_id']
            if Quiz.objects.filter(quiz_id__exact=quiz_id).first():
                messages.error(request, "Quiz Id already exists!", extra_tags='alert alert-warning alert-dismissible fade show')
                return render(request, self.template_name, {'form': form,'update': False})
            instance = form.save(commit=False)
            teacher = Teacher.objects.get(user=request.user)
            instance.teacher = teacher
            instance.save()
            form = CreateQuizForm()
            messages.error(request, "Successfully Created Quiz",
                           extra_tags='alert alert-success alert-dismissible fade show')
            return redirect('polls:quiz-list')
        else:
            messages.error(request, "Error", extra_tags='alert alert-warning alert-dismissible fade show')
        context = {
            'form': form,
            'update': False
        }
        return render(request, self.template_name, context)


class QuizListView(View):
    template_name = 'teacher/quiz_list.html'

    def get(self, request):
        teacher = Teacher.objects.filter(user=request.user).first()
        object_list = Quiz.objects.filter(teacher=teacher)
        context = {
            'object_list': object_list,
        }
        return render(request, self.template_name, context)


class QuizDetailView(View):
    template_name = 'teacher/quiz_detail.html'

    def get(self, request, quiz_pk):
        context = {}

        if id is not None:
            quiz_object = Quiz.objects.get(id=quiz_pk)
            question_list = Poll.objects.filter(quiz=quiz_object)
            context['object'] = quiz_object
            context['question_list'] = question_list
        return render(request, self.template_name, context)


class QuizUpdateView(View):
    template_name = 'teacher/create_quiz.html'

    def get_object(self):
        id = self.kwargs.get('quiz_pk')
        obj = None
        if id is not None:
            obj = get_object_or_404(Quiz, id=id)
        return obj

    def get(self, request, *args, **kwargs):

        context = {}
        obj = self.get_object()
        if obj is not None:
            form = CreateQuizForm(instance=obj)
            context['form'] = form
            context['update'] = True

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = {}
        obj = self.get_object()
        if obj is not None:
            form = CreateQuizForm(request.POST, instance=obj)
            if form.is_valid():
                quiz_id = form.cleaned_data['quiz_id']
                # if Quiz.objects.filter(quiz_id__exact=quiz_id).first():
                #     messages.error(request, "Quiz Id already exists!",
                #                    extra_tags='alert alert-warning alert-dismissible fade show')
                #     return render(request, self.template_name, {'form': form, 'update': False})

                form.save()
                form = CreateQuizForm()
                quiz_object = Quiz.objects.get(id=self.kwargs.get('quiz_pk'))
                question_list = Poll.objects.filter(quiz=quiz_object)
                context['question_list'] = question_list
            context['object'] = obj
            context['update'] = True

        return render(request, 'teacher/quiz_detail.html', context)


class AddToClassroom(View):
    template_name = 'teacher/add_to_classroom.html'

    def get(self, request, quiz_pk):
        quiz = get_object_or_404(Quiz, id=quiz_pk)
        teacher = Teacher.objects.filter(user=request.user).first()
        object_list = Classroom.objects.filter(teacher=teacher)
        context = {
            'quiz': quiz,
            'classrooms': object_list
        }
        return render(request, self.template_name, context)

    def post(self, request, quiz_pk):
        classroom_list = request.POST.get('classroom_list')
        classroom = Classroom.objects.filter(id=classroom_list).first()
        quiz = Quiz.objects.filter(id=quiz_pk).first()

        if quiz.classroom == None:
            quiz.classroom = classroom
            quiz.save()
            messages.error(request, f"Quiz Added in {quiz.classroom.c_name}",
                           extra_tags='alert alert-success alert-dismissible fade show')
            return redirect('polls:quiz-list')
        else:
            messages.error(request, f"Already quiz Active in {quiz.classroom.c_name}",
                       extra_tags='alert alert-success alert-dismissible fade show')
        context = {}
        return redirect('polls:quiz-to-classroom', quiz_pk=quiz_pk)


class AddQuestionView(View):
    template_name = 'teacher/add_question.html'

    def get(self, request, *args, **kwargs):
        form = CHOICES()
        context = {
            'form': form
        }
        return render(request, self.template_name, context)
#
#     def post(self, request, quiz_id, *args, **kwargs):
#         form = CHOICES(request.POST)
#         if form.is_valid():
#             correct_ans_no = form.cleaned_data.get('NUMS')
#             question = request.POST.get('question')
#             option1 = request.POST.get('option1')
#             option2 = request.POST.get('option2')
#             option3 = request.POST.get('option3')
#             option4 = request.POST.get('option4')
#
#             if correct_ans_no == 1:
#                 correct_ans = option1
#             elif correct_ans_no == 2:
#                 correct_ans = option2
#             elif correct_ans_no == 3:
#                 correct_ans = option3
#             else:
#                 correct_ans = option4
#
#             id = self.kwargs.get('quiz_id')
#
#             quiz_object = Quiz.objects.get(id=id)
#
#             question_obj = Question(quiz=quiz_object, correct_ans=correct_ans, question_text=question)
#             question_obj.save()
#
#             option1_obj = QuestionOption(question=question_obj, option=option1)
#             option1_obj.save()
#
#             option2_obj = QuestionOption(question=question_obj, option=option2)
#             option2_obj.save()
#
#             option3_obj = QuestionOption(question=question_obj, option=option3)
#             option3_obj.save()
#
#             option4_obj = QuestionOption(question=question_obj, option=option4)
#             option4_obj.save()
#
#             question_list = Question.objects.filter(quiz=quiz_object)
#
#             context = {
#                 'object': quiz_object,
#                 'question_list': question_list,
#
#             }
#             return render(request, 'teacher/quiz_detail.html', context)
#
#         return render(request, self.template_name)


@login_required
def students_attempted(request, quiz_pk, poll_id):

    poll = Poll.objects.get(id__exact=poll_id)
    vote_set = poll.vote_set.all()
    context = {
        'quiz_pk': quiz_pk,
        'poll_id': poll_id,
        'vote_set': vote_set
    }

    return render(request, 'teacher/students_attempted.html', context)


@login_required()
def classroom_detail(request, class_pk):
    classroom = Classroom.objects.filter(id=class_pk).first()
    quiz_list = Quiz.objects.filter(classroom=classroom)
    studies_in = classroom.studiesin_set.all()
    students_list = []

    for object in studies_in:
        students_list.append(object.student)

    context = {
        'student_list': students_list,
        'classroom': classroom,
        'quiz_list': quiz_list
    }

    return render(request, 'teacher/classroom_detail.html', context)

@login_required()
def remove_classroom(request, quiz_pk):
    quiz = Quiz.objects.filter(id=quiz_pk).first()
    quiz.classroom = None
    quiz.save()
    return redirect('polls:quiz-to-classroom', quiz_pk=quiz_pk)

@login_required()
def student_classroom_detail(request, class_pk):
    classroom = Classroom.objects.filter(id=class_pk).first()
    quiz_set = classroom.quiz_set.all()

    context = {
        'classroom': classroom,
        'quiz_set': quiz_set
    }

    return render(request, 'student/classroom_detail.html',context)