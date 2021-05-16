from django.db import models
import secrets
import random
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.


class Teacher(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)


class Classroom(models.Model):

    c_name = models.CharField(max_length=100)
    class_id = models.CharField(max_length=100)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)


class Quiz(models.Model):
    quiz_name = models.CharField(max_length=100)
    quiz_id = models.CharField(max_length=50)
    active = models.BooleanField(default=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return self.quiz_id

    def get_absolute_url(self):
        return reverse('polls:quiz-detail', kwargs={'quiz_pk': self.id})


class Poll(models.Model):

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text = models.TextField()
    active = models.BooleanField(default=True)

    def user_can_vote(self, user):

        user_votes = user.vote_set.all()
        qs = user_votes.filter(poll=self)
        if qs.exists():
            return False
        return True

    @property
    def get_vote_count(self):
        return self.vote_set.count()

    def __str__(self):
        return self.text
    #
    # def get_result_dict(self):
    #     res=[]
    #     for choice in self.choice_set.all():
    #         d={}
    #         alert_class=['primary', 'secondary', 'success',
    #                        'danger', 'dark', 'warning', 'info']
    #         d['alert_class']=secrets.choice(alert_class)
    #         d['text']=choice.choice_text
    #         d['num_votes']=choice.get_vote_count
    #         if not self.get_vote_count:
    #             d['percentage'] = 0
    #         else:
    #             d['percentage'] = (choice.get_vote_count /
    #                                self.get_vote_count)*100
    #
    #         res.append(d)
    #     return res


class Question(models.Model):

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_text = models.TextField()
    correct_ans = models.TextField()
    option1 = models.TextField()
    option2 = models.TextField()
    option3 = models.TextField()
    option4 = models.TextField()


class Choice(models.Model):

    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice_text = models.TextField()
    @property
    def get_vote_count(self):
        return self.vote_set.count()

    def __str__(self):
        return f"{self.poll.text[:25]}-{self.choice_text[:25]}"


class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    roll_no = models.CharField(max_length=20)
    class_name = models.CharField(max_length=20)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    pid = models.CharField(max_length=20)


class Result(models.Model):
    score = models.CharField(max_length=20)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)


class StudiesIn(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)


class ChoosedOption(models.Model):
    result = models.ForeignKey(Result, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    option = models.TextField()


# class Choice(models.Model):
#     poll = models.ForeignKey(Poll,on_delete=models.CASCADE)
#     choice_text=models.CharField(max_length=200)
#
#     @property
#     def get_vote_count(self):
#         return self.vote_set.count()
#
#     def __str__(self):
#         return f"{self.poll.text[:25]}-{self.choice_text[:25]}"
#
#
class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.poll.text[:25]}-{self.choice.choice_text[:25]}  "

