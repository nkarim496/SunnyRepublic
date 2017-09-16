from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Book(models.Model):
    link = models.URLField(verbose_name='ссылка', help_text='Ссылка на учебный материал')
    title = models.CharField(max_length=200, verbose_name='название', help_text='Название материала')

    def __str__(self):
        return self.title


class Teacher(models.Model):
    user = models.OneToOneField(User)
    pic = models.ImageField(verbose_name='аватарка', blank=True, upload_to='profile_images')
    description = models.TextField(verbose_name='о преподавателе')
    phone = models.CharField(max_length=20, blank=True)
    cite = models.CharField(max_length=400, blank=True)

    def __str__(self):
        return "Teacher: " + self.user.username


class Student(models.Model):
    user = models.OneToOneField(User)
    teacher = models.ForeignKey(Teacher, blank=True)
    books = models.ManyToManyField(Book, blank=True)
    pic = models.ImageField(verbose_name='аватарка', blank=True, upload_to='profile_images')
    cite = models.CharField(max_length=400, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    rate = models.PositiveIntegerField(verbose_name='рейтинг', blank=True)  # todo как сделать по умолчанию None
    cash = models.IntegerField(blank=True)  # todo как сделать по умолчанию None
    visits = models.IntegerField(blank=True)  # todo как сделать по умолчанию None

    def __str__(self):
        return "Student: " + self.user.username


class Lesson(models.Model):
    title = models.CharField(max_length=400, verbose_name='Тема занятия')
    students = models.ManyToManyField(Student)
    teacher = models.ForeignKey(Teacher, default=1)
    date = models.DateTimeField(verbose_name='дата занятия', default=timezone.now)
    homework = models.TextField(verbose_name='домашнее задание', blank=True)

    def __str__(self):
        return self.title + " " + str(self.date)


class Value(models.Model):
    student = models.ForeignKey(Student)
    lesson = models.ForeignKey(Lesson)
    value = models.IntegerField(verbose_name='оценка', help_text='от -3 до 3', blank=True)
    comment = models.TextField(verbose_name='комментарий', blank=True)

    def __str__(self):
        return self.student.user.username + " " + str(self.value)
