from django import forms
from .models import Orcamento, TipoMaterial, Batida, CoeficienteFator, TabelaPreco


class OrcamentoForm(forms.ModelForm):
    """Formulário para criar/editar orçamentos"""
    
    class Meta:
        model = Orcamento
        fields = [
            'cliente', 'tipo_cliente', 'endereco', 'cidade', 'uf', 'cep',
            'telefone', 'email', 'numero_pedido', 'data_previsao_entrega',
            'tipo_material', 'batida', 'largura_mm', 'comprimento_mm',
            'tipo_corte', 'textura', 'cor_urdume', 'quantidade_metros', 'tabela_manual_metragem',
            'acabamento', 'tem_ultrassonico',
            'observacoes', 'marca', 'valor_frete',
        ]
        widgets = {
            'cliente': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Nome do cliente',
            }),
            'tipo_cliente': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                '@change': 'calcularValores()',
            }),
            'endereco': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Endereço completo',
            }),
            'cidade': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Cidade',
            }),
            'uf': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'UF',
                'maxlength': '2',
            }),
            'cep': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': '00000-000',
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': '(00) 00000-0000',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'email@exemplo.com',
            }),
            'numero_pedido': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Número do pedido',
            }),
            'data_previsao_entrega': forms.DateInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'type': 'date',
            }),
            'vendedor': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Nome do vendedor',
            }),
            'tipo_material': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                '@change': 'calcularValores()',
                'onchange': 'carregarBatidasMaterial(this.value)'
            }),
            'batida': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'id': 'id_batida',
                '@change': 'calcularValores()',
            }),
            'largura_mm': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Largura em mm',
                '@input': 'calcularValores()',
                'min': '1',
            }),
            'comprimento_mm': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Comprimento em mm',
                '@input': 'calcularValores()',
                'min': '1',
            }),
            'tipo_corte': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                '@change': 'calcularValores()',
            }),
            'textura': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            }),
            'cor_urdume': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            }),
            'quantidade_metros': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Quantidade em metros',
                '@input': 'calcularValores()',
                'min': '1',
            }),
            'tabela_manual_metragem': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            }),
            'quantidade_unidades': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Quantidade de unidades',
                'x-model': 'orcamento.quantidade_unidades',
                '@input': 'calcularValores()',
                'min': '1',
            }),
            'unidades_por_pacote': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Unidades por pacote',
                'min': '1',
            }),
            'acabamento': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                '@change': 'calcularValores()',
            }),
            'tem_ultrassonico': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-blue-600 rounded focus:ring-2 focus:ring-blue-500',
                '@change': 'calcularValores()',
            }),
            'observacoes': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Observações adicionais',
                'rows': 4,
            }),
            'marca': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Marca',
            }),
            'valor_frete': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0',
            }),
        }


class TipoMaterialForm(forms.ModelForm):
    """Formulário para Tipo de Material"""
    class Meta:
        model = TipoMaterial
        fields = ['nome', 'codigo', 'ordem', 'ativo']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Ex: Tafetá, Sarja, Canvas'
            }),
            'codigo': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Ex: TAFETA, SARJA'
            }),
            'ordem': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'min': '0'
            }),
            'ativo': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-blue-600 rounded focus:ring-2 focus:ring-blue-500'
            }),
        }


class BatidaForm(forms.ModelForm):
    """Formulário para Batida"""
    class Meta:
        model = Batida
        fields = ['tipo_material', 'numero_batidas', 'descricao', 'ordem', 'ativo']
        widgets = {
            'tipo_material': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500'
            }),
            'numero_batidas': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Ex: 20, 25, 28',
                'min': '1'
            }),
            'descricao': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Ex: 20 batidas (gerado automaticamente se vazio)'
            }),
            'ordem': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'min': '0'
            }),
            'ativo': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-blue-600 rounded focus:ring-2 focus:ring-blue-500'
            }),
        }


class CoeficienteFatorForm(forms.ModelForm):
    """Formulário para Coeficientes Fator"""

    class Meta:
        model = CoeficienteFator
        fields = ['tipo_material', 'codigo_corte', 'largura', 'coeficiente']
        widgets = {
            'tipo_material': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500'
            }),
            'codigo_corte': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500'
            }),
            'largura': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'min': '1'
            }),
            'coeficiente': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'step': '0.00001',
                'min': '0'
            })
        }


class TabelaPrecoForm(forms.ModelForm):
    """Formulário para Tabela de Preço"""
    class Meta:
        model = TabelaPreco
        fields = ['metragem', 'tipo_material', 'preco_metro']
        widgets = {
            'metragem': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'min': '1',
                'placeholder': 'Ex: 100, 500, 1000'
            }),
            'tipo_material': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500'
            }),
            'preco_metro': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'step': '0.01',
                'min': '0.01',
                'placeholder': 'R$ 0.00'
            })
        }