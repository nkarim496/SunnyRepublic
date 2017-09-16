from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.cache import never_cache
from sunny.models import Student, Lesson, Book, Teacher, Value
from sunny.forms import PictureChangeForm
from django.http import Http404
from datetime import datetime
import os


def is_student(user):
    """checks if the user in Students group"""
    return user.groups.filter(name='Students').exists()


def is_teacher(user):
    """checks if the user in Teachers group"""
    return user.groups.filter(name='Teachers').exists()


@login_required
def index(request):
    if is_student(request.user):
        return redirect('student_home')
    elif is_teacher(request.user):
        return redirect('teacher_home')
    else:
        raise Http404("Neither a student or a teacher doesn't exist")


@login_required
def student_home(request):
    try:
        student = Student.objects.get(user__pk=request.user.pk)
    except Student.DoesNotExist:
        raise Http404("User with id={} doesn't exist.".format(request.user.pk))

    # '-date' сортирует от поздних дат к ранним, 'date' от ранних к поздним
    lessons = student.lesson_set.filter(date__lte=datetime.now()).order_by('-date')[:5]
    values = []
    for lesson in lessons:
        value = Value.objects.filter(lesson=lesson, student=student).first()
        values.append(value)
    les_val = zip(lessons, values)  # связываем оценки с уроками в лист таплов

    nxt = student.lesson_set.filter(date__gte=datetime.now()).order_by('date').first()
    print("Next lesson: {}".format(nxt))
    if nxt:
        teacher = nxt.teacher
    else:
        teacher = None

    context = {'student': student, 'teacher': teacher, 'nxt': nxt,
               'molodec': round((100 * student.cash) / (student.visits * 3)),
               'les_val': les_val}  # участников достаю из лессонс. катит с .all в конце

    return render(request, 'sunny/student_home.html', context)


@login_required
@user_passes_test(is_student)
def student_lessons(request):
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        raise Http404("User with id={} doesn't exist.".format(request.user.pk))

    # '-date' сортирует от поздних дат к ранним ( первый в сете 1.09.2017, второй 1.08.2017)
    # 'date' от ранних к поздним ( первый в сете 1.08.2017, второй 1.09.2017)
    lessons = student.lesson_set.filter(date__lte=datetime.now()).order_by('-date')[:10]
    values = []
    for lesson in lessons:
        value = Value.objects.filter(lesson=lesson, student=student).first()
        values.append(value)
    les_val = zip(lessons, values)  # связываем оценки с уроками в лист таплов

    nxt = student.lesson_set.filter(date__gte=datetime.now()).order_by('date').first()
    print("Next lesson: {}".format(nxt))
    if nxt:
        teacher = nxt.teacher
    else:
        teacher = None

    context = {'student': student, 'teacher': teacher, 'nxt': nxt,
               'molodec': round((100 * student.cash) / (student.visits * 3)),
               'les_val': les_val}  # участников достаю из лессонс. катит с .all в конце

    return render(request, 'sunny/student_lessons.html', context)


@login_required
def change_picture(request):
    changed = False
    if request.method == 'POST':
        form = PictureChangeForm(request.POST, request.FILES)
        if form.is_valid():
            profile = request.user.student
            old_image_path = profile.pic.path
            profile.pic = request.FILES['picture']
            profile.save()
            os.unlink(old_image_path)  # delete old image from system
            changed = True
    else:
        form = PictureChangeForm()
    return render(request, 'sunny/change_picture.html', {'form': form, 'changed': changed})


@login_required
def student_lessons_ajax(request):
    context = {}
    if request.method == 'GET':
        offset = int(request.GET['offset'])
        student = Student.objects.get(user=request.user)
        lessons = student.lesson_set.filter(date__lte=datetime.now()).order_by('-date')[offset:offset+offset]
        values = []
        for lesson in lessons:
            value = Value.objects.filter(lesson=lesson, student=student).first()
            values.append(value)
        context['les_val'] = zip(lessons, values)
    return render(request, 'sunny/lessons_ajax.html', context)
