from django import forms
from django.forms import widgets
from .models import Classroom, Teacher, Student, Quiz, Poll, Choice
from django.contrib.admin.widgets import AdminSplitDateTime

NUMS = [
    (1, 'Option 1'),
    (2, 'Option 2'),
    (3, 'Option 3'),
    (4, 'Option 4'),
    ]


class CHOICES(forms.Form):

    NUMS = forms.CharField(widget=forms.RadioSelect(choices=NUMS, attrs={'class': "form-check-input"}))


class CreateQuizForm(forms.ModelForm):
    quiz_name = forms.CharField(label='Quiz Name', widget=forms.TextInput(attrs={'placeholder': 'Quiz Name'}))
    quiz_id = forms.CharField(label='Quiz Id', widget=forms.TextInput(attrs={'placeholder': 'Quiz id'}))
    active = forms.BooleanField(label='Active', required=False)
    start_time = forms.SplitDateTimeField(widget=AdminSplitDateTime())
    end_time = forms.SplitDateTimeField(widget=AdminSplitDateTime())

    class Meta:
        model = Quiz
        fields = [
            'quiz_name',
            'quiz_id',
            'active',
            'start_time',
            'end_time',
        ]


class CreateStudentForm(forms.ModelForm):

    first_name = forms.CharField(label='First Name', widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(label='Last Name', widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    class_name = forms.CharField(label='Class Name', widget=forms.TextInput(attrs={'placeholder': 'Class'}))
    roll_no = forms.CharField(label='Roll No', widget=forms.TextInput(attrs={'placeholder': 'Roll No'}))
    pid = forms.CharField(label='PID', widget=forms.TextInput(attrs={'placeholder': 'PID'}))

    class Meta:
        model = Student
        fields = [
            'first_name',
            'last_name',
            'class_name',
            'roll_no',
            'pid'
        ]


class CreateClassroomForm(forms.ModelForm):
    c_name = forms.CharField(label='Name', widget=forms.TextInput(attrs={'placeholder': 'Classroom Name'}))
    class_id = forms.CharField(label='Class Id', widget=forms.TextInput(attrs={'placeholder': 'Classroom ID'}))

    class Meta:
        model = Classroom
        fields = [
            'c_name',
            'class_id',

        ]


class CreateTeacherForm(forms.ModelForm):
    first_name = forms.CharField(label='FirstName', widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(label='LastName', widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))

    class Meta:
        model = Teacher
        fields = [
            'first_name',
            'last_name'
        ]


class PollAddForm(forms.ModelForm):

    choice1 = forms.CharField(max_length=150, min_length=1, label='Choice 1',
    widget=forms.TextInput(attrs={'class':'form-control'}))

    choice2 = forms.CharField(max_length=150 ,min_length=1, label='Choice 2',
    widget = forms.TextInput(attrs={'class':'form-control'}))

    choice3 = forms.CharField(max_length=150, min_length=1, label='Choice 3',
    widget=forms.TextInput(attrs={'class':'form-control'}))

    choice4 = forms.CharField(max_length=150, min_length=1, label='Choice 4',
    widget=forms.TextInput(attrs={'class':'form-control'}))

    # NUMS = forms.CharField(widget=forms.RadioSelect(choices=NUMS, attrs={}))

    class Meta:
        model = Poll
        fields = ['text', 'choice1', 'choice2', 'choice3', 'choice4']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'cols': 20}),
        }


class EditPollForm(forms.ModelForm):

    class Meta:
        model = Poll
        fields = ['text', ]
        widgets = {
            'text': forms.Textarea(attrs={'class':'form-control', 'rows': 5, 'cols': 20})
        }


class EditChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text', ]
        widgets = {
            'choice_text': forms.TextInput(attrs={'class':'form-control'})
        }


class ChoiceAddForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text', ]
        widgets = {
            'choice_text': forms.TextInput(attrs={'class': 'form-control', })
        }


class EnterQuizForm(forms.Form):

    quiz_id = forms.CharField(label='Quiz_id',max_length=10,min_length=5,
                            widget=forms.TextInput(attrs={'class': 'form-control'}))

