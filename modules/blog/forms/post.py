from django import forms
from django.utils.text import slugify
from ..domain.post import BlogPost, Category, Tag

class BlogPostForm(forms.ModelForm):
    tags_input = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Digite as tags separadas por vírgula',
            'class': 'form-control'
        }),
        help_text='Separe as tags com vírgulas'
    )
    
    class Meta:
        model = BlogPost
        fields = [
            'title', 'content', 'excerpt', 'category',
            'featured_image', 'status', 'is_featured',
            'meta_description', 'meta_keywords'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'excerpt': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'featured_image': forms.FileInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'meta_description': forms.TextInput(attrs={'class': 'form-control'}),
            'meta_keywords': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        self.company = kwargs.pop('company', None)
        super().__init__(*args, **kwargs)
        
        # Filtrar categorias ativas
        self.fields['category'].queryset = Category.objects.filter(is_active=True)
        
        # Preencher tags se editando
        if self.instance.pk:
            tags = self.instance.tags.all()
            self.fields['tags_input'].initial = ', '.join([tag.name for tag in tags])
    
    def clean_title(self):
        title = self.cleaned_data['title']
        slug = slugify(title)
        
        # Verificar se slug já existe (exceto para o próprio post)
        existing = BlogPost.objects.filter(slug=slug)
        if self.instance.pk:
            existing = existing.exclude(pk=self.instance.pk)
        
        if existing.exists():
            raise forms.ValidationError('Já existe um post com este título.')
        
        return title
    
    def save(self, commit=True):
        post = super().save(commit=False)
        
        if self.company:
            post.company = self.company
        
        if commit:
            post.save()
            
            # Processar tags
            tags_input = self.cleaned_data.get('tags_input', '')
            if tags_input:
                tag_names = [name.strip() for name in tags_input.split(',') if name.strip()]
                tags = []
                for tag_name in tag_names:
                    tag, created = Tag.objects.get_or_create(
                        name=tag_name,
                        defaults={'slug': slugify(tag_name)}
                    )
                    tags.append(tag)
                post.tags.set(tags)
            else:
                post.tags.clear()
        
        return post