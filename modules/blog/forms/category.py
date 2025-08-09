from django import forms
from django.utils.text import slugify
from ..domain.post import Category


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description', 'color', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome da categoria'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Descrição da categoria (opcional)'
            }),
            'color': forms.TextInput(attrs={
                'type': 'color',
                'class': 'form-control',
                'value': '#007bff'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
    
    def clean_name(self):
        name = self.cleaned_data['name']
        slug = slugify(name)
        
        # Verificar se slug já existe (exceto para a própria categoria)
        existing = Category.objects.filter(slug=slug)
        if self.instance.pk:
            existing = existing.exclude(pk=self.instance.pk)
        
        if existing.exists():
            raise forms.ValidationError('Já existe uma categoria com este nome.')
        
        return name
    
    def clean_color(self):
        color = self.cleaned_data['color']
        if not color.startswith('#'):
            color = f'#{color}'
        
        # Validar formato hexadecimal
        if len(color) != 7:
            raise forms.ValidationError('Cor deve estar no formato hexadecimal (#RRGGBB)')
        
        try:
            int(color[1:], 16)
        except ValueError:
            raise forms.ValidationError('Cor deve estar no formato hexadecimal válido')
        
        return color
