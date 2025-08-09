from django import forms
from django.utils.text import slugify
from ..domain.post import Tag


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome da tag'
            })
        }
    
    def clean_name(self):
        name = self.cleaned_data['name']
        slug = slugify(name)
        
        # Verificar se slug já existe (exceto para a própria tag)
        existing = Tag.objects.filter(slug=slug)
        if self.instance.pk:
            existing = existing.exclude(pk=self.instance.pk)
        
        if existing.exists():
            raise forms.ValidationError('Já existe uma tag com este nome.')
        
        return name
