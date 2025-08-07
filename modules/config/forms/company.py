from django import forms
from django.utils.text import slugify
from ..domain.company import Company

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = [
            'name', 'email', 'phone', 'address', 
            'domain', 'logo', 'is_active'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'domain': forms.TextInput(attrs={'class': 'form-control'}),
            'logo': forms.FileInput(attrs={'class': 'form-control'}),
        }
    
    def clean_email(self):
        email = self.cleaned_data['email']
        existing = Company.objects.filter(email=email)
        if self.instance.pk:
            existing = existing.exclude(pk=self.instance.pk)
        
        if existing.exists():
            raise forms.ValidationError('Este e-mail já está em uso.')
        
        return email