from django import forms
from .models import Todo
from django.forms.widgets import SelectDateWidget,DateTimeBaseInput,SplitDateTimeWidget
from django.utils.timezone import datetime



class TodoForm(forms.ModelForm):

    class Meta:
        model=Todo

        fields = ['title','image','desc','important','datecompleted']

