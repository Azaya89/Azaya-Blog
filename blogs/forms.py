from django import forms
from .models import BlogPost, Entry

class BlogForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title']
        labels = {'title': ''}

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text': 'Entry:'}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}