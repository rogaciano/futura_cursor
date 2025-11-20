from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import (
    TipoMaterial, TipoCorte, TabelaPreco, CoeficienteFator,
    ValorGoma, ValorCorte, Configuracao, Orcamento, Textura, Vendedor,
    CorOrcamento, Batida, Fita
)


class BatidaInline(admin.TabularInline):
    """Inline para gerenciar batidas de cada material"""
    model = Batida
    extra = 1
    fields = ['numero_batidas', 'descricao', 'ordem', 'ativo']
    ordering = ['ordem', 'numero_batidas']


@admin.register(TipoMaterial)
class TipoMaterialAdmin(admin.ModelAdmin):
    list_display = ['nome', 'codigo', 'ordem', 'get_batidas_disponiveis', 'ativo']
    list_editable = ['ordem', 'ativo']
    search_fields = ['nome', 'codigo']
    list_filter = ['ativo']
    ordering = ['ordem', 'nome']
    inlines = [BatidaInline]
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'codigo', 'ordem', 'ativo'),
            'description': 'Defina as batidas disponíveis para este material na seção abaixo.'
        }),
    )
    
    def get_batidas_disponiveis(self, obj):
        """Mostra as batidas disponíveis para o material"""
        batidas = obj.batidas.filter(ativo=True).values_list('numero_batidas', flat=True)
        if batidas:
            return ', '.join(f"{b}" for b in batidas)
        return "—"
    get_batidas_disponiveis.short_description = "Batidas Disponíveis"


@admin.register(Batida)
class BatidaAdmin(admin.ModelAdmin):
    list_display = ['tipo_material', 'numero_batidas', 'descricao', 'ordem', 'ativo']
    list_editable = ['numero_batidas', 'descricao', 'ordem', 'ativo']
    list_filter = ['tipo_material', 'ativo']
    search_fields = ['tipo_material__nome', 'descricao']
    ordering = ['tipo_material', 'ordem', 'numero_batidas']
    
    fieldsets = (
        (None, {
            'fields': ('tipo_material', 'numero_batidas', 'descricao', 'ordem', 'ativo'),
            'description': 'Cada material pode ter várias opções de batidas. '
                         'Ex: Tafetá pode ter 20, 25 ou 28 batidas.'
        }),
    )


@admin.register(Fita)
class FitaAdmin(admin.ModelAdmin):
    list_display = ['largura_mm', 'fator']
    list_editable = ['fator']
    ordering = ['largura_mm']
    
    fieldsets = (
        (None, {
            'fields': ('largura_mm', 'fator'),
            'description': 'Tabela de Fatores (FITAS - Plan2). '
                         'Define o fator de rendimento baseado na largura da fita.'
        }),
    )


@admin.register(TipoCorte)
class TipoCorteAdmin(admin.ModelAdmin):
    list_display = ['nome', 'codigo', 'codigo_calc', 'ativo']
    list_editable = ['ativo']
    search_fields = ['nome', 'codigo']
    list_filter = ['ativo']


@admin.register(TabelaPreco)
class TabelaPrecoAdmin(admin.ModelAdmin):
    list_display = ['metragem', 'tipo_material', 'preco_metro']
    list_editable = ['preco_metro']
    list_filter = ['tipo_material']
    search_fields = ['tipo_material__nome']
    ordering = ['tipo_material', 'metragem']
    
    fieldsets = (
        (None, {
            'fields': ('metragem', 'tipo_material', 'preco_metro'),
            'description': 'Tabela de preços por metragem para cada tipo de material. '
                         'O sistema escolhe automaticamente o preço baseado na quantidade de metros do pedido.'
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('tipo_material')


@admin.register(CoeficienteFator)
class CoeficienteFatorAdmin(admin.ModelAdmin):
    list_display = ['largura', 'tipo_material', 'codigo_corte', 'coeficiente']
    list_editable = ['coeficiente']
    list_filter = ['tipo_material', 'codigo_corte']
    search_fields = ['tipo_material__nome', 'codigo_corte__nome']
    ordering = ['tipo_material', 'largura']
    
    fieldsets = (
        (None, {
            'fields': ('largura', 'tipo_material', 'codigo_corte', 'coeficiente'),
            'description': 'Coeficientes que afetam o cálculo do preço baseado em largura, material e tipo de corte.'
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('tipo_material', 'codigo_corte')


@admin.register(ValorGoma)
class ValorGomaAdmin(admin.ModelAdmin):
    list_display = ['largura', 'goma_fino', 'goma_grosso', 'termocolante']
    list_editable = ['goma_fino', 'goma_grosso', 'termocolante']
    ordering = ['largura']
    
    fieldsets = (
        (None, {
            'fields': ('largura', 'goma_fino', 'goma_grosso', 'termocolante'),
            'description': 'Valores adicionais de goma baseados na largura e tipo de goma selecionado.'
        }),
    )


@admin.register(ValorCorte)
class ValorCorteAdmin(admin.ModelAdmin):
    list_display = ['largura', 'canvas', 'cetim']
    list_editable = ['canvas', 'cetim']
    ordering = ['largura']
    
    fieldsets = (
        (None, {
            'fields': ('largura', 'canvas', 'cetim'),
            'description': 'Valores especiais de corte para materiais Canvas e Cetim baseados na largura.'
        }),
    )


@admin.register(Configuracao)
class ConfiguracaoAdmin(admin.ModelAdmin):
    list_display = ['chave', 'valor', 'descricao', 'tipo_dado']
    list_editable = ['valor']
    search_fields = ['chave', 'descricao']
    list_filter = ['tipo_dado']
    
    fieldsets = (
        (None, {
            'fields': ('chave', 'valor', 'tipo_dado', 'descricao'),
            'description': 'Configurações globais do sistema. Altere com cuidado pois afetam todos os cálculos.'
        }),
    )
    
    def has_delete_permission(self, request, obj=None):
        # Não permitir deletar configurações
        return False


class CorOrcamentoInline(admin.TabularInline):
    """Inline para adicionar cores ao orçamento"""
    model = CorOrcamento
    extra = 1
    fields = ['posicao', 'densidade', 'codigo_cor', 'quantidade_unidades', 'quantidade_demais', 'ordem']
    ordering = ['densidade', 'ordem', 'posicao']


@admin.register(CorOrcamento)
class CorOrcamentoAdmin(admin.ModelAdmin):
    list_display = [
        'orcamento', 'posicao', 'densidade', 'codigo_cor',
        'quantidade_unidades', 'quantidade_demais', 'total_unidades'
    ]
    list_filter = ['densidade', 'posicao']
    search_fields = ['orcamento__numero_pedido', 'codigo_cor']
    ordering = ['orcamento', 'densidade', 'ordem']


@admin.register(Orcamento)
class OrcamentoAdmin(admin.ModelAdmin):
    list_display = [
        'numero_pedido', 'cliente', 'vendedor', 'tipo_material', 'data_emissao',
        'valor_total', 'ativo'
    ]
    list_filter = [
        'tipo_material', 'tipo_cliente', 'vendedor', 'data_emissao', 'ativo'
    ]
    search_fields = ['cliente', 'numero_pedido', 'observacoes', 'vendedor__nome_completo']
    date_hierarchy = 'data_emissao'
    readonly_fields = [
        'valor_metro', 'valor_milheiro', 'valor_unidade', 'valor_total',
        'criado_em', 'atualizado_em'
    ]
    autocomplete_fields = ['vendedor']
    inlines = [CorOrcamentoInline]
    
    fieldsets = (
        ('Informações do Cliente', {
            'fields': (
                'cliente', 'tipo_cliente', 'endereco', 'cidade', 'uf', 'cep',
                'telefone', 'email'
            )
        }),
        ('Dados do Orçamento', {
            'fields': (
                'numero_pedido', 'data_emissao', 'data_previsao_entrega', 'vendedor'
            )
        }),
        ('Especificações do Produto', {
            'fields': (
                'tipo_material', 'largura_mm', 'comprimento_mm', 'tipo_corte',
                'cor_urdume', 'marca'
            )
        }),
        ('Quantidades', {
            'fields': (
                'quantidade_metros', 'quantidade_unidades', 'unidades_por_pacote', 'tabela_manual_metragem'
            )
        }),
        ('Opções', {
            'fields': (
                'tem_goma', 'tipo_goma', 'tem_ultrassonico'
            )
        }),
        ('Valores Calculados', {
            'fields': (
                'valor_metro', 'valor_milheiro', 'valor_unidade', 'valor_total',
                'valor_frete'
            )
        }),
        ('Observações', {
            'fields': ('observacoes',),
            'classes': ('collapse',)
        }),
        ('Controle', {
            'fields': ('ativo', 'criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Textura)
class TexturaAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nome', 'ordem', 'ativo']
    list_editable = ['ordem', 'ativo']
    search_fields = ['codigo', 'nome', 'descricao']
    list_filter = ['ativo']
    ordering = ['ordem', 'codigo']


@admin.register(Vendedor)
class VendedorAdmin(admin.ModelAdmin):
    list_display = [
        'nome_completo', 'user', 'email', 'telefone',
        'comissao_percentual', 'meta_mensal', 'ativo'
    ]
    list_filter = ['ativo', 'data_admissao']
    search_fields = ['nome_completo', 'email', 'cpf', 'user__username']
    readonly_fields = ['data_admissao']
    
    fieldsets = (
        ('Informações do Usuário', {
            'fields': ('user', 'nome_completo', 'email', 'telefone', 'cpf')
        }),
        ('Configurações de Vendas', {
            'fields': ('comissao_percentual', 'meta_mensal')
        }),
        ('Controle', {
            'fields': ('ativo', 'data_admissao', 'observacoes')
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('user')
