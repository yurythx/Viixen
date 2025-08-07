from django import forms
from ..domain.post import BlogPost, Category, Tag

class BlogPostForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False
    )
    
    class Meta:
        model = BlogPost
        fields = [
            'title', 'content', 'excerpt', 'category', 'tags', 
            'featured_image', 'status', 'is_featured', 
            'meta_description', 'meta_keywords'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'excerpt': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'featured_image': forms.FileInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'meta_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'meta_keywords': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'Título',
            'content': 'Conteúdo',
            'excerpt': 'Resumo',
            'category': 'Categoria',
            'tags': 'Tags',
            'featured_image': 'Imagem Destacada',
            'status': 'Status',
            'is_featured': 'Post em Destaque',
            'meta_description': 'Meta Descrição',
            'meta_keywords': 'Palavras-chave',
        }
    
    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company', None)
        super().__init__(*args, **kwargs)
        
        if company:
            self.fields['category'].queryset = Category.objects.filter(is_active=True)