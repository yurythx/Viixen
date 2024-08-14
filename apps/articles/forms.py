from django import forms
from tinymce.widgets import TinyMCE

from .models import Article


class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
         return False


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'exerpt', 'content', 'cover', 'category', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Título', 'class': 'form-control form-control-lg'}),
            'exerpt': forms.Textarea(attrs={'placeholder': 'Súmario', 'class': 'form-control form-control-lg'}),
            'content': TinyMCE(attrs={'required': False, 'cols': 30, 'rows': 10, 'class': 'form-control', 'id': 'mytextarea'}),
            'cover': forms.FileInput(attrs={'id': 'validatedCustomFile'}),
            'category': forms.Select(attrs={'placeholder': 'Categoria', 'class': 'form-control form-control-lg'}),
            'tags': forms.Select(attrs={'placeholder': 'Tags', 'class': 'form-control form-control-lg'}),
        }