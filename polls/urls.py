from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
from django.views.i18n import JavaScriptCatalog


app_name = "polls"

urlpatterns = [

    path('quiz/', views.quiz, name='quiz'),
    path('<int:quiz_pk>/list/', views.polls_list, name='list'),
    path('quiz/<int:quiz_pk>/add/', views.polls_add, name='addPoll'),
    path('quiz/<int:quiz_pk>/edit/<int:poll_id>/', views.polls_edit, name='edit'),
    path('quiz/<int:quiz_pk>/delete/<int:poll_id>/', views.polls_delete, name='delete_poll'),

    path('quiz/<int:quiz_pk>/edit/<int:poll_id>/choice/<int:choice_id>/', views.choice_edit, name='choice_edit'),

    path('quiz/<int:quiz_pk>/detail/<int:poll_id>/', views.poll_detail, name='detail'),
    path('quiz/<int:quiz_pk>/Votedetail/<int:poll_id>/', views.vote_detail, name='vote-detail'),
    path('quiz/<int:quiz_pk>/endquiz/', views.end_quiz, name='end-quiz'),
    path('quiz/<int:quiz_pk>/endpoll/<int:poll_id>/', views.end_poll, name='end-poll'),
    path('quiz/<int:quiz_pk>/vote/<int:poll_id>/', views.poll_vote, name='vote'),
    path('quiz/<int:quiz_pk>/resultsdata/<int:poll_id>/', views.resultsData, name='resultsdata'),
    path('quiz/<int:quiz_pk>/teacherresultsdata/<int:poll_id>/', views.teacher_resultsData, name='teacher-resultsdata'),

    # Teacher
    path('teacher/classroom/create/', login_required(views.ClassroomCreateView.as_view()), name='create-classroom'),
    path('teacher/', login_required(views.TeacherHomeView.as_view()), name='teacher-homepage'),
    path('teacher/create/', login_required(views.CreateTeacherView.as_view()), name='create-teacher'),
    path('teacher/classroom/list/', login_required(views.ClassroomListView.as_view()), name='classroom-list'),
    path('teacher/classroom/delete/<int:class_pk>/', views.classroom_delete, name='classroom-delete'),
    path('teacher/classroom/detail/<int:class_pk>/', views.classroom_detail, name='classroom-detail'),



    # teacher quiz
    path('teacher/quiz/create/', login_required(views.CreateQuizView.as_view()), name='create-quiz'),
    path('teacher/quiz/list/', login_required(views.QuizListView.as_view()), name='quiz-list'),
    path('teacher/quiz/detail/<int:quiz_pk>/', login_required(views.QuizDetailView.as_view()), name='quiz-detail'),
    path('teacher/quiz/update/<int:quiz_pk>/', login_required(views.QuizUpdateView.as_view()), name='quiz-update'),
    path('teacher/quiz/<int:quiz_pk>/addQuestion/', login_required(views.AddQuestionView.as_view()), name='add-question'),
    path('teacher/quiz/<int:quiz_pk>/delete/', views.quiz_delete, name='quiz-delete'),
    path('teacher/quiz/<int:quiz_pk>/addToClassroom/', login_required(views.AddToClassroom.as_view()), name='quiz-to-classroom'),
    path('teacher/quiz/<int:quiz_pk>/removeClassroom/', views.remove_classroom, name='remove-classroom'),
    path('teacher/quiz/<int:quiz_pk>/students-attempted/<int:poll_id>/', views.students_attempted, name='students-attempted'),






    # Student
    path('student/', login_required(views.StudentHomeView.as_view()), name='student-homepage'),
    path('student/create/', login_required(views.CreateStudentView.as_view()), name='create-student'),
    path('student/classroom/join/', login_required(views.EnterClassroomView.as_view()), name='join-classroom'),
    path('student/classroom/list/', login_required(views.StudentClassroomListView.as_view()), name='student-classroom-list'),
    path('student/classroom/detail/<int:class_pk>/',views.student_classroom_detail , name='student-classroom-detail'),

    path('jsi18n', JavaScriptCatalog.as_view(), name='js-catlog'),


]