from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from sunny.models import Student, Lesson, Book, Teacher, Value
from sunny.forms import PictureChangeForm, LessonForm, ValueForm
from django.http import Http404
from datetime import datetime
import os


def is_student(user):
    """checks if the user in Students group"""
    return user.groups.filter(name='Students').exists()


def is_teacher(user):
    """checks if the user in Teachers group"""
    return user.groups.filter(name='Teachers').exists()


def search_students(starts_with):
    """returns queryset of 10 students whose names start with starts_with
        не пашет istartswith, проблема в sqlite. на postgresql будет пахать"""
    students = None
    starts_with = starts_with.split(' ')
    if len(starts_with) == 1:
        students = Student.objects.filter(user__first_name__istartswith=starts_with[0]).order_by('user__first_name')[:10]
        if students.count() == 0:
            students = Student.objects.filter(user__last_name__istartswith=starts_with[0]).order_by('user__last_name')[:10]
            if students.count() == 0:
                students = None
    elif len(starts_with) == 2:
        students = Student.objects.filter(user__first_name__istartswith=starts_with[0],
                                          user__last_name__istartswith=starts_with[1]).order_by('user__first_name')[:10]
        if students.count() == 0:
            students = Student.objects.filter(user__first_name__istartswith=starts_with[1],
                                              user__last_name__istartswith=starts_with[0]).order_by('user__last_name')[:10]
            if students.count() == 0:
                students = None
    return students


@login_required
def index(request):
    if is_student(request.user):
        return redirect('student_home')
    elif is_teacher(request.user):
        return redirect('teacher_home')
    else:
        raise Http404("Neither a student or a teacher is in the groups")


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
    count_l = student.lesson_set.count()
    values = []
    for lesson in lessons:
        value = Value.objects.filter(lesson=lesson, student=student).first()
        values.append(value)
    les_val = zip(lessons, values)  # связываем оценки с уроками в лист таплов

    nxt = student.lesson_set.filter(date__gte=datetime.now()).order_by('date').first()
    if nxt:
        teacher = nxt.teacher
    else:
        teacher = None

    context = {'student': student, 'teacher': teacher, 'nxt': nxt, 'count_l': count_l,
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
        lessons = student.lesson_set.filter(date__lte=datetime.now()).order_by('-date')[offset:offset+10]
        values = []
        for lesson in lessons:
            value = Value.objects.filter(lesson=lesson, student=student).first()
            values.append(value)
        context['les_val'] = zip(lessons, values)
    return render(request, 'sunny/lessons_ajax.html', context)


@login_required
@user_passes_test(is_student)
def student_books(request):
    student = Student.objects.get(user=request.user)
    books = student.books.all().order_by('title')
    return render(request, 'sunny/student_books.html', {'student': student, 'books': books})


@login_required
def student_top(request):
    top_3 = Student.objects.all().order_by('rate')[:3]
    top_students = Student.objects.all().order_by('rate')[3:]
    return render(request, 'sunny/student_top.html', {'top_3': top_3, 'top_students': top_students})


@login_required
def student_page(request, username):
    try:
        student = Student.objects.get(user__username=username)
    except Student.DoesNotExist:
        raise Http404("Student with username '{}' doesn't exist".format(username))
    values = student.value_set.all().order_by('-lesson__date')[:5]
    count_v = student.value_set.count()
    return render(request, 'sunny/student_page.html', {'student': student, 'values': values,
                                                       'count_v': count_v})


@login_required
def get_values_ajax(request):
    values = []
    if request.method == 'GET':
        offset_start = int(request.GET['offsetStart'])
        offset_end = int(request.GET['offsetEnd'])
        username = request.GET['username']
        values = Value.objects.filter(student__user__username=username).order_by('-lesson__date')[offset_start:offset_end]
    return render(request, 'sunny/get_values_ajax.html', {'values': values})


@login_required
@user_passes_test(is_teacher)
def teacher_home(request):
    try:
        teacher = Teacher.objects.get(user=request.user)
    except Teacher.DoesNotExist:
        raise Http404("User with username '{}' isn't a teacher.".format(request.user.username))

    # большой гемор чтобы найти непроставленные оценки
    teacher_lessons = teacher.lesson_set.all().order_by('-date')  # все занятия учителя
    need_value = []
    for lesson in teacher_lessons:
        lesson_students = lesson.students.all()  # все участники каждого занятия учителя
        for student in lesson_students:
            # если у студента нет оценки за занятие у учителя, добавляем в лист
            if not student.value_set.filter(lesson=lesson).exists():
                need_value.append({'lesson': lesson, 'student': student})

    # todo осторировать need_value по дате. можно побробовать sort с ключом

    # последние пять занятий отсортированных от дальней к ближней к 2000 году и следующее занятие
    lessons = teacher.lesson_set.filter(date__lte=datetime.now()).order_by('-date')[:5]
    nxt = teacher.lesson_set.filter(date__gte=datetime.now()).order_by('date').first()

    return render(request, 'sunny/teacher_home.html', {'teacher': teacher, 'nxt': nxt, 'lessons': lessons,
                                                       'need_value': need_value})


@login_required
def teacher_page(request, username):
    try:
        teacher = Teacher.objects.get(user__username=username)
    except Teacher.DoesNotExist:
        raise Http404("Teacher with username '{}' doesn't exist".format(username))
    students = teacher.student_set.all()
    values = teacher.value_set.all().order_by('-lesson__date')[:5]
    count_v = teacher.value_set.count()
    return render(request, 'sunny/teacher_page.html', {'teacher': teacher, 'values': values, 'students': students,
                                                       'count_v': count_v})


@login_required
def lesson_page(request, lesson_id):
    try:
        lesson = Lesson.objects.get(pk=lesson_id)
    except Lesson.DoesNotExist:
        raise Http404("Lesson doesn't exist")

    # собираем студентов и их оценки
    students = lesson.students.all()
    students_values = []
    for student in students:
        if Value.objects.filter(student=student, lesson=lesson).exists():
            value = Value.objects.get(student=student, lesson=lesson)
            students_values.append((student, value))
        else:
            students_values.append((student, None))

    return render(request, "sunny/lesson_page.html", {'lesson': lesson,
                                                      'students_values': students_values})


@login_required
@user_passes_test(is_teacher)
def lesson_add(request):
    form = LessonForm()
    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            teacher = Teacher.objects.get(user=request.user)
            lesson = Lesson(title=form.cleaned_data['title'], homework=form.cleaned_data['homework'],
                            date=datetime.combine(form.cleaned_data['date'], form.cleaned_data['time']),
                            teacher=teacher)
            lesson.save()
            if form.cleaned_data['students']:
                students_pks = set(form.cleaned_data['students'])
                for student_pk in students_pks:
                    student = Student.objects.get(pk=student_pk)
                    lesson.students.add(student)
            lesson.save()
            return redirect('lesson_page', lesson_id=lesson.pk)
        else:
            print(form.errors)
    return render(request, 'sunny/lesson_add.html', {'form': form})


@login_required
@user_passes_test(is_teacher)
def student_search(request):
    students = None
    if request.method == 'GET':
        starts_with = request.GET['starts_with']
        if starts_with:
            students = search_students(starts_with)
    return render(request, 'sunny/student_list.html', {'students': students})


@login_required
@user_passes_test(is_teacher)
def lesson_edit(request, lesson_id):
    try:
        lesson = Lesson.objects.get(pk=lesson_id)
    except Lesson.DoesNotExist:
        raise Http404("Lesson doesn't exist")

    values = Value.objects.filter(lesson=lesson)

    # делим студентов с оценками и без оценок
    students = lesson.students.all()
    students_with_values = []
    students_without_values = []
    for student in students:
        if Value.objects.filter(student=student, lesson=lesson).exists():
            value = Value.objects.get(student=student, lesson=lesson)
            students_with_values.append((student, value))
        else:
            students_without_values.append(student)

    form = LessonForm(initial={'title': lesson.title,
                               'homework': lesson.homework,
                               'date': lesson.date.date(),
                               'time': lesson.date.time().isoformat('minutes'),
                               'students': ','.join([str(student.pk) for student in students])})

    # Если занятие прошло, то нельзя его изменить
    editable = True
    if datetime.now().date() > lesson.date.date():
        editable = False

    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid() and editable:
            teacher = Teacher.objects.get(user=request.user)
            lesson.teacher = teacher
            lesson.title = form.cleaned_data['title']
            lesson.homework = form.cleaned_data['homework']
            lesson.date = datetime.combine(form.cleaned_data['date'], form.cleaned_data['time'])
            print(lesson)
            if form.cleaned_data['students']:
                students_pks = set(form.cleaned_data['students'])
                lesson.students.clear()
                for student_pk in students_pks:
                    print(student_pk)
                    student = Student.objects.get(pk=student_pk)
                    print(student)
                    lesson.students.add(student)
            lesson.save()
            print(lesson.pk)
            return redirect('lesson_page', lesson_id=lesson.pk)
        else:
            print(form.errors)
    return render(request, 'sunny/lesson_edit.html', {'form': form, 'students': students,
                                                      'lesson': lesson, 'editable': editable,
                                                      'values': values,
                                                      'students_with_values': students_with_values,
                                                      'students_without_values': students_without_values})


@login_required
@user_passes_test(is_teacher)
def value_add(request, username, lesson_id):
    try:
        student = Student.objects.get(user__username=username)
        lesson = Lesson.objects.get(pk=lesson_id)
        teacher = Teacher.objects.get(user=request.user)
    except Student.DoesNotExist:
        raise Http404("Student doesn't exist")
    except Lesson.DoesNotExist:
        raise Http404("Lesson doesn't exist")
    except Teacher.DoesNotExist:
        raise Http404("Teacher doesn't exist")

    # если оценка уже есть, то изменить нельзя
    editable = True
    if Value.objects.filter(student=student, lesson=lesson).exists():
        editable = False

    form = ValueForm()
    if request.method == 'POST':
        form = ValueForm(request.POST)
        if form.is_valid() and editable:
            new_value = Value(student=student, teacher=teacher, lesson=lesson,
                              value=form.cleaned_data['value'],
                              comment=form.cleaned_data['comment'])
            new_value.save()
            return redirect('lesson_edit', lesson_id=lesson.pk)
        else:
            print(form.errors)
            print("Editable: {}".format(editable))
    return render(request, 'sunny/value_add.html', {'lesson': lesson, 'student': student,
                                                    'form': form})


@login_required
@user_passes_test(is_teacher)
def lesson_delete(request, lesson_id):
    try:
        lesson = Lesson.objects.get(pk=lesson_id)
    except Lesson.DoesNotExist:
        raise Http404("Lesson doesn't exist")

    # можно удалить только если занятие еще не состоялось
    if lesson.date >= datetime.now():
        lesson.delete()
    else:
        print("Нельзя удалить состоявшийся урок.")
    return redirect('teacher_home')
