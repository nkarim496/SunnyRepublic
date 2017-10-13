from django import forms
from sunny.models import Lesson, Value
from datetime import datetime
from django.core import validators
from django.core.exceptions import ValidationError

# Comma Separated Values Form Field for Django.
# There are CommaSeparatedCharField(returns list of chars), CommaSeparatedIntegerField(returns list of integers).
# https://gist.github.com/eerien/7002396


class MinLengthValidator(validators.MinLengthValidator):
    message = 'Ensure this value has at least %(limit_value)d elements (it has %(show_value)d).'


class MaxLengthValidator(validators.MaxLengthValidator):
    message = 'Ensure this value has at most %(limit_value)d elements (it has %(show_value)d).'


class CommaSeparatedCharField(forms.Field):
    def __init__(self, dedup=True, max_length=None, min_length=None, *args, **kwargs):
        self.dedup, self.max_length, self.min_length = dedup, max_length, min_length
        super(CommaSeparatedCharField, self).__init__(*args, **kwargs)
        if min_length is not None:
            self.validators.append(MinLengthValidator(min_length))
        if max_length is not None:
            self.validators.append(MaxLengthValidator(max_length))

    def to_python(self, value):
        if value in validators.EMPTY_VALUES:
            return []

        value = [item.strip() for item in value.split(',') if item.strip()]
        if self.dedup:
            value = list(set(value))

        return value

    def clean(self, value):
        value = self.to_python(value)
        self.validate(value)
        self.run_validators(value)
        return value


class CommaSeparatedIntegerField(forms.Field):
    default_error_messages = {
        'invalid': 'Enter comma separated numbers only.',
    }

    def __init__(self, dedup=True, max_length=None, min_length=None, *args, **kwargs):
        self.dedup, self.max_length, self.min_length = dedup, max_length, min_length
        super(CommaSeparatedIntegerField, self).__init__(*args, **kwargs)
        if min_length is not None:
            self.validators.append(MinLengthValidator(min_length))
        if max_length is not None:
            self.validators.append(MaxLengthValidator(max_length))

    def to_python(self, value):
        if value in validators.EMPTY_VALUES:
            return []

        try:
            value = [int(item.strip()) for item in value.split(',') if item.strip()]
            if self.dedup:
                value = list(set(value))
        except (ValueError, TypeError):
            raise ValidationError(self.error_messages['invalid'])

        return value

    def clean(self, value):
        value = self.to_python(value)
        self.validate(value)
        self.run_validators(value)
        return value


class PictureChangeForm(forms.Form):
    picture = forms.ImageField()


class LessonForm(forms.ModelForm):
    date = forms.DateField(label='Дата',
                           initial=datetime.now().date(),
                           widget=forms.DateInput(attrs={'class': 'form-control',
                                                         'type': 'date'}),
                           error_messages={'invalid': 'Неверный формат даты. Введите ДД.ММ.ГГГГ.'},
                           input_formats=['%d.%m.%Y',
                                          '%d-%m-%Y',
                                          '%Y-%m-%d',
                                          '%d/%m/%Y'])
    time = forms.TimeField(label='Время',
                           initial=datetime.now().time().isoformat('minutes'),
                           error_messages={'invalid': 'Неверный формат времени. Введите ЧЧ:ММ.'},
                           widget=forms.TimeInput(attrs={'class': 'form-control',
                                                         'type': 'time'}),
                           input_formats=['%H:%M:%S',
                                          '%H:%M'])
    students = CommaSeparatedIntegerField(widget=forms.HiddenInput())

    class Meta:
        model = Lesson
        fields = ('title', 'homework')
        widgets = {'title': forms.TextInput(attrs={'class': 'form-control'}),
                   'homework': forms.Textarea(attrs={'class': 'form-control',
                                                     'rows': 10})}


class ValueForm(forms.ModelForm):
    class Meta:
        model = Value
        fields = ('comment', 'value')
        widgets = {'value': forms.RadioSelect(),
                   'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 10})}
