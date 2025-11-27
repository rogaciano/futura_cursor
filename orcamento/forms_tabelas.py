from django import forms
from .models import Acabamento, PrecoAcabamento

class AcabamentoForm(forms.ModelForm):
    """Formulário para Acabamento"""
    class Meta:
        model = Acabamento
        fields = ['nome', 'codigo', 'ordem', 'ativo']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Ex: Goma F, Cola Fria'
            }),
            'codigo': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Ex: GOMA_F'
            }),
            'ordem': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'min': '0'
            }),
            'ativo': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-blue-600 rounded focus:ring-2 focus:ring-blue-500'
            }),
        }

class PrecoAcabamentoForm(forms.ModelForm):
    """Formulário para Preço de Acabamento"""
    class Meta:
        model = PrecoAcabamento
        fields = ['acabamento', 'largura_mm', 'preco']
        widgets = {
            'acabamento': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500'
            }),
            'largura_mm': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'min': '1',
                'placeholder': 'Largura máxima em mm'
            }),
            'preco': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'step': '0.00001',
                'min': '0',
                'placeholder': 'R$ 0.00000'
            }),
        }

