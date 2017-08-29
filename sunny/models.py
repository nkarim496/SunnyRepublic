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
    whatsapp = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.user.username


class Student(models.Model):
    user = models.OneToOneField(User)
    teacher = models.ForeignKey(Teacher, blank=True)
    books = models.ManyToManyField(Book, blank=True)
    pic = models.ImageField(verbose_name='аватарка', blank=True, upload_to='profile_images')

    def __str__(self):
        return self.user.username


class Lesson(models.Model):
    student = models.ForeignKey(Student)
    date = models.DateTimeField(verbose_name='дата оценки', default=timezone.now)
    homework = models.TextField(verbose_name='домашка', blank=True)
    value = models.PositiveSmallIntegerField(verbose_name='оценка',
                                             help_text='Положительное целое число от 1 до 10',
                                             blank=True)  # todo пока от 1 до 10, потом надо додумать
    comm = models.TextField(verbose_name='комментарий', blank=True)

    def __str__(self):
        return self.student.user.username + str(self.date)
