from django import forms
from django.utils.text import slugify
from ..domain.page import Page


class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = [
            'title', 'content', 'excerpt', 'featured_image', 
            'is_published', 'meta_description'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título da página'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 15,
                'placeholder': 'Conteúdo da página'
            }),
            'excerpt': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Resumo da página (opcional)'
            }),
            'featured_image': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'is_published': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'meta_description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Descrição para SEO (máx. 160 caracteres)',
                'maxlength': 160
            })
        }
    
    def clean_title(self):
        title = self.cleaned_data['title']
        slug = slugify(title)
        
        # Verificar se slug já existe (exceto para a própria página)
        existing = Page.objects.filter(slug=slug)
        if self.instance.pk:
            existing = existing.exclude(pk=self.instance.pk)
        
        if existing.exists():
            raise forms.ValidationError('Já existe uma página com este título.')
        
        return title
