from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from sunny.models import Student, Lesson, Book
from sunny.forms import PictureChangeForm
import os


@login_required
def index(request):
    try:
        homework = Lesson.objects.filter(student__user=request.user).order_by('-date').first()  # todo Домашка должна выходить ближайшая поздняя к тудэй
    except Homework.DoesNotExist:
        homework = None
    # books = request.user.userprofile.books.all()
    books = Book.objects.filter(student__user=request.user)
    return render(request, 'sunny/index.html', {'homework': homework, 'books': books})


@login_required
def progress(request):
    lessons = Lesson.objects.filter(student__user=request.user).order_by('-date')
    high_value_count = lessons.filter(value=5).count()
    molodec = (100 * high_value_count) // len(lessons)
    return render(request, 'sunny/progress.html', {'values': lessons,
                                                   'high_value_count': high_value_count,
                                                   'molodec': molodec})


@login_required
def homeworks_show(request):
    user = request.user
    homeworks = Lesson.objects.filter(student__user=user).order_by('-date')
    books = Book.objects.filter(student__user=user)
    return render(request, 'sunny/homeworks.html', {'homeworks': homeworks,
                                                    'books': books})


@login_required
def profile_settings(request):
    return render(request, 'sunny/profile_settings.html')


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

