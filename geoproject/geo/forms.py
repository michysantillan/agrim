from django import forms
from .models import Area
from django.contrib.auth.forms import UserCreationForm


class DynamicForm:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fields = ['CheckboxInput', 'ClearableFileInput', 'FileInput']
        for field in self.fields:
            widget_name = self.fields[field].widget.__class__.__name__
            if widget_name not in fields:
                self.fields[field].widget.attrs.update({
                    'class': 'form-control'
                })


class AreaForm(DynamicForm, forms.ModelForm):
    
    class Meta:
        model = Area
        fields = ('name',)

