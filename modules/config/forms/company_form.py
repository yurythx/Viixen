from django import forms
from ..domain.company import Company

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'email', 'phone', 'address', 'domain', 'logo']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'domain': forms.URLInput(attrs={'class': 'form-control'}),
            'logo': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Nome da Empresa',
            'email': 'Email',
            'phone': 'Telefone',
            'address': 'Endereço',
            'domain': 'Domínio',
            'logo': 'Logo',
        }