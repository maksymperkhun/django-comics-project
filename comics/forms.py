# comics/forms.py
from django import forms
from .models import Comic

class ComicForm(forms.ModelForm):
    class Meta:
        model = Comic
        fields = '__all__'
