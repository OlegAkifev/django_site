import string

from django import forms
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.deconstruct import deconstructible

from .models import Category, Husband


# @deconstructible
# class RussianValidator:
#     ALLOWED_CHARS = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя0123456789- '
#     code = 'russian'
#
#     def __init__(self, message=None):
#         self.message = message if message else "Должны присутствовать только русские символы или пробел"
#
#     def __call__(self, value, *args, **kwargs):
#         if not (set(value) <= set(self.ALLOWED_CHARS)):
#             raise forms.ValidationError(self.message, code=self.code)


class AddPostForm(forms.Form):
    title = forms.CharField(max_length=255, min_length=5,
                            label='Заголовок', widget=forms.TextInput(attrs={'class': 'form-input'}),
                            error_messages={'min_length': 'Слишком короткий заголовок',
                                            'required': 'Без заголовка никак'},
                            )
    slug = forms.SlugField(max_length=255,
                           validators=[
                               MinLengthValidator(5, message='Минимум 5 символов'),
                               MaxLengthValidator(100, message='Максимум 100 символов'),
                           ])
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 50, 'rows': 5}), required=False, label='Текст статьи')
    is_published = forms.BooleanField(required=False, initial=True, label='Опубликовано')
    category = forms.ModelChoiceField(queryset=Category.objects.all(),
                                      label='Категория', empty_label='Категория не выбрана')
    husband = forms.ModelChoiceField(queryset=Husband.objects.all(), required=False,
                                     label='Муж', empty_label='Не замужем')

    def clean_title(self):
        title = self.cleaned_data['title']
        ALLOWED_CHARS = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя0123456789- '
        if not (set(title) <= set(ALLOWED_CHARS)):
            raise forms.ValidationError("Должны присутствовать только русские символы или пробел")
