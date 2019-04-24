from django import forms
from .models import Todo

class TodoForm(forms.ModelForm):
    taskdate = forms.DateTimeField(input_formats=['%m/%d/%Y %H:%M:%S'])
    class Meta:
        model = Todo
        fields = ("description", "taskdate", "complete",)
