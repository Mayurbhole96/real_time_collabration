from django import forms
from .models import Document

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter document title'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Start typing here...', 'rows': 10}),
        }
