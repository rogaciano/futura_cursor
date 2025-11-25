from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal


class TipoMaterial(models.Model):
    """Tipos de material: Tafetá, Sarja, Alta Definição, etc."""
    nome = models.CharField(max_length=100, unique=True)
    codigo = models.CharField(max_length=20, unique=True)
    ordem = models.IntegerField(default=0)
    ativo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Tipo de Material'
        verbose_name_plural = 'Tipos de Material'
        ordering = ['ordem', 'nome']
    
    def __str__(self):
        return self.nome


class Batida(models.Model):
    """
    Opções de batidas disponíveis para cada tipo de material.
    Cada material pode ter várias opções de batidas (ex: Tafetá: 20, 25, 28)
    """
    tipo_material = models.ForeignKey(
        TipoMaterial,
        on_delete=models.CASCADE,
        related_name='batidas',
        help_text="Material ao qual esta opção de batida pertence"
    )
    numero_batidas = models.IntegerField(
        validators=[MinValueValidator(1)],
        help_text="Número de batidas (ex: 20, 25, 28)"
    )
    descricao = models.CharField(
        max_length=100,
        blank=True,
        help_text="Descrição adicional (ex: '20 batidas', '28 batidas')"
    )
    ordem = models.IntegerField(
        default=0,
        help_text="Ordem de exibição"
    )
    ativo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Batida'
        verbose_name_plural = 'Batidas'
        ordering = ['tipo_material', 'ordem', 'numero_batidas']
        unique_together = [['tipo_material', 'numero_batidas']]
    
    def __str__(self):
        return f"{self.tipo_material.nome} - {self.numero_batidas} batidas"
    
    def save(self, *args, **kwargs):
        # Auto-gerar descrição se não fornecida
        if not self.descricao:
            self.descricao = f"{self.numero_batidas} batidas"
        super().save(*args, **kwargs)


class TipoCorte(models.Model):
    """Tipos de corte: Normal, Meio Corte, Dobra Meio, Dobra Cantos, etc."""
    nome = models.CharField(max_length=100, unique=True)
    codigo = models.CharField(max_length=30, unique=True)
    codigo_calc = models.IntegerField(help_text="Código usado nos cálculos (baseado no comprimento do nome)")
    ativo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Tipo de Corte'
        verbose_name_plural = 'Tipos de Corte'
        ordering = ['nome']
    
    def __str__(self):
        return self.nome


class TabelaPreco(models.Model):
    """Tabela de preços por metragem e tipo de material"""
    metragem = models.IntegerField(validators=[MinValueValidator(1)])
    tipo_material = models.ForeignKey(TipoMaterial, on_delete=models.CASCADE, related_name='precos')
    preco_metro = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    
    class Meta:
        verbose_name = 'Tabela de Preço'
        verbose_name_plural = 'Tabelas de Preços'
        ordering = ['metragem', 'tipo_material']
        unique_together = ['metragem', 'tipo_material']
    
    def __str__(self):
        return f'{self.metragem}m - {self.tipo_material.nome}: R$ {self.preco_metro}'


class CoeficienteFator(models.Model):
    """Coeficientes de fator baseados em largura e tipo"""
    largura = models.IntegerField(validators=[MinValueValidator(1)], help_text="Largura em mm")
    tipo_material = models.ForeignKey(TipoMaterial, on_delete=models.CASCADE, related_name='coeficientes')
    codigo_corte = models.ForeignKey(TipoCorte, on_delete=models.CASCADE, related_name='coeficientes')
    coeficiente = models.DecimalField(max_digits=10, decimal_places=5, validators=[MinValueValidator(Decimal('0.0'))])
    
    class Meta:
        verbose_name = 'Coeficiente Fator'
        verbose_name_plural = 'Coeficientes Fator'
        ordering = ['largura', 'tipo_material']
        unique_together = ['largura', 'tipo_material', 'codigo_corte']
    
    def __str__(self):
        return f'{self.largura}mm - {self.tipo_material.nome} - {self.codigo_corte.nome}: {self.coeficiente}'


class ValorGoma(models.Model):
    """Valores de goma por largura"""
    largura = models.IntegerField(unique=True, validators=[MinValueValidator(1)])
    goma_fino = models.DecimalField(max_digits=10, decimal_places=5, default=Decimal('0.0'))
    goma_grosso = models.DecimalField(max_digits=10, decimal_places=5, default=Decimal('0.0'))
    termocolante = models.DecimalField(max_digits=10, decimal_places=5, default=Decimal('0.0'))
    
    class Meta:
        verbose_name = 'Valor de Goma'
        verbose_name_plural = 'Valores de Goma'
        ordering = ['largura']
    
    def __str__(self):
        return f'{self.largura}mm'


class ValorCorte(models.Model):
    """Valores de corte especial por largura"""
    largura = models.IntegerField(unique=True, validators=[MinValueValidator(1)])
    canvas = models.DecimalField(max_digits=10, decimal_places=5, default=Decimal('0.0'))
    cetim = models.DecimalField(max_digits=10, decimal_places=5, default=Decimal('0.0'))
    
    class Meta:
        verbose_name = 'Valor de Corte'
        verbose_name_plural = 'Valores de Corte'
        ordering = ['largura']
    
    def __str__(self):
        return f'{self.largura}mm'


class Acabamento(models.Model):
    """
    Materiais de acabamento (Célula O25 da planilha)
    Ex: Goma F, Goma G, Cola Fria, Termocolante, etc.
    """
    nome = models.CharField(max_length=100, unique=True)
    codigo = models.CharField(max_length=50, unique=True)
    ordem = models.IntegerField(default=0)
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Acabamento / Material'
        verbose_name_plural = 'Acabamentos / Materiais'
        ordering = ['ordem', 'nome']

    def __str__(self):
        return self.nome


class PrecoAcabamento(models.Model):
    """
    Preço do acabamento por largura (Plan2)
    Substitui ValorGoma e ValorCorte antigos
    """
    largura_mm = models.IntegerField(validators=[MinValueValidator(1)])
    acabamento = models.ForeignKey(Acabamento, on_delete=models.CASCADE, related_name='precos')
    preco = models.DecimalField(max_digits=10, decimal_places=5, validators=[MinValueValidator(Decimal('0.0'))])

    class Meta:
        verbose_name = 'Preço de Acabamento'
        verbose_name_plural = 'Preços de Acabamentos'
        ordering = ['largura_mm', 'acabamento']
        unique_together = ['largura_mm', 'acabamento']

    def __str__(self):
        return f'{self.largura_mm}mm - {self.acabamento.nome}: R$ {self.preco}'


class Vendedor(models.Model):
    """Vendedor do sistema - vinculado ao User do Django"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='vendedor')
    nome_completo = models.CharField(max_length=200)
    telefone = models.CharField(max_length=20, blank=True)
    email = models.EmailField()
    cpf = models.CharField(max_length=14, blank=True, help_text="000.000.000-00")
    data_admissao = models.DateField(auto_now_add=True)
    ativo = models.BooleanField(default=True)
    comissao_percentual = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=Decimal('5.0'),
        help_text="Percentual de comissão sobre vendas"
    )
    meta_mensal = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=Decimal('0.0'),
        help_text="Meta de vendas mensal em R$"
    )
    observacoes = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Vendedor'
        verbose_name_plural = 'Vendedores'
        ordering = ['nome_completo']
    
    def __str__(self):
        return self.nome_completo
    
    @property
    def is_gestor(self):
        """Verifica se o vendedor é gestor"""
        return self.user.groups.filter(name='Gestor').exists()
    
    def total_vendas_mes(self):
        """Retorna o total de vendas do mês atual"""
        from django.db.models import Sum
        from datetime import datetime
        
        hoje = datetime.now().date()
        mes_atual = hoje.replace(day=1)
        
        total = Orcamento.objects.filter(
            vendedor=self,
            data_emissao__gte=mes_atual,
            ativo=True
        ).aggregate(total=Sum('valor_total'))['total']
        
        return total or Decimal('0.0')
    
    def percentual_meta(self):
        """Retorna o percentual da meta atingida"""
        if self.meta_mensal <= 0:
            return 0
        return (self.total_vendas_mes() / self.meta_mensal) * 100


class Configuracao(models.Model):
    """Configurações globais do sistema"""
    chave = models.CharField(max_length=100, unique=True)
    valor = models.TextField()
    descricao = models.TextField(blank=True)
    tipo_dado = models.CharField(
        max_length=20,
        choices=[
            ('decimal', 'Decimal'),
            ('integer', 'Inteiro'),
            ('text', 'Texto'),
            ('boolean', 'Booleano'),
        ],
        default='text'
    )
    
    class Meta:
        verbose_name = 'Configuração'
        verbose_name_plural = 'Configurações'
        ordering = ['chave']
    
    def __str__(self):
        return f'{self.chave}: {self.valor}'
    
    def get_valor(self):
        """Retorna o valor convertido para o tipo correto"""
        if self.tipo_dado == 'decimal':
            return Decimal(self.valor)
        elif self.tipo_dado == 'integer':
            return int(self.valor)
        elif self.tipo_dado == 'boolean':
            return self.valor.lower() in ('true', '1', 'yes', 'sim')
        return self.valor


class Orcamento(models.Model):
    """Orçamento de etiquetas"""
    TABELA_METRAGEM_CHOICES = [
        (300, '300 m'),
        (500, '500 m'),
        (1000, '1.000 m'),
        (2500, '2.500 m'),
        (5000, '5.000 m'),
        (10000, '10.000 m'),
        (15000, '15.000 m'),
    ]
    TIPO_CLIENTE_CHOICES = [
        ('industria_novo', 'Indústria Novo'),
        ('industria_antigo', 'Indústria Antigo'),
        ('comercio_novo', 'Comércio Novo'),
        ('comercio_antigo', 'Comércio Antigo'),
    ]
    
    COR_URDUME_CHOICES = [
        ('branco', 'Branco'),
        ('preto', 'Preto'),
        ('branco_preto', 'Branco e Preto'),
        ('vermelho', 'Vermelho'),
        ('nenhum', 'Nenhum'),
    ]
    
    # Informações do Cliente
    cliente = models.CharField(max_length=200)
    tipo_cliente = models.CharField(max_length=20, choices=TIPO_CLIENTE_CHOICES, default='comercio_novo')
    endereco = models.CharField(max_length=300, blank=True)
    cidade = models.CharField(max_length=100, blank=True)
    uf = models.CharField(max_length=2, blank=True)
    cep = models.CharField(max_length=10, blank=True)
    telefone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    
    # Dados do Orçamento
    numero_pedido = models.CharField(max_length=50, blank=True)
    data_emissao = models.DateField(auto_now_add=True)
    data_previsao_entrega = models.DateField(null=True, blank=True)
    vendedor = models.ForeignKey(
        Vendedor, 
        on_delete=models.PROTECT, 
        related_name='orcamentos',
        null=True,
        blank=True,
        help_text="Vendedor responsável pelo orçamento"
    )
    
    # Especificações do Produto
    tipo_material = models.ForeignKey(TipoMaterial, on_delete=models.PROTECT)
    batida = models.ForeignKey(
        'Batida',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        help_text="Número de batidas selecionado para este material"
    )
    largura_mm = models.IntegerField(validators=[MinValueValidator(1)], help_text="Largura em mm")
    comprimento_mm = models.IntegerField(validators=[MinValueValidator(1)], help_text="Comprimento em mm")
    tipo_corte = models.ForeignKey(TipoCorte, on_delete=models.PROTECT)
    textura = models.ForeignKey(
        'Textura',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        help_text="Textura selecionada para a etiqueta"
    )
    cor_urdume = models.CharField(max_length=20, choices=COR_URDUME_CHOICES, default='nenhum')
    
    # Quantidades
    quantidade_metros = models.IntegerField(validators=[MinValueValidator(1)], help_text="Metros - DIGITADO pelo usuário")
    quantidade_unidades = models.IntegerField(default=1, validators=[MinValueValidator(1)], help_text="Unidades - CALCULADO automaticamente")
    milheiros = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.0'), help_text="Milheiros - CALCULADO = ARREDONDAR.PARA.BAIXO(Unidades/1000,2)")
    unidades_por_pacote = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    tabela_manual_metragem = models.IntegerField(
        choices=TABELA_METRAGEM_CHOICES,
        null=True,
        blank=True,
        help_text="Override manual da faixa de metragem (Planilha T11). Se vazio, usa a metragem digitada."
    )
    
    # Opções
    acabamento = models.ForeignKey(
        'Acabamento',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Material / Acabamento selecionado (ex: Goma, Termocolante)"
    )
    tem_ultrassonico = models.BooleanField(default=False)
    
    # Valores Calculados
    valor_metro = models.DecimalField(max_digits=10, decimal_places=5, default=Decimal('0.0'))
    valor_milheiro = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.0'))
    valor_unidade = models.DecimalField(max_digits=10, decimal_places=5, default=Decimal('0.0'))
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.0'))
    valor_frete = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.0'))
    
    # Observações
    observacoes = models.TextField(blank=True)
    marca = models.CharField(max_length=100, blank=True)
    
    # Controle
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    ativo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Orçamento'
        verbose_name_plural = 'Orçamentos'
        ordering = ['-data_emissao', '-criado_em']
    
    def __str__(self):
        return f'Orçamento {self.numero_pedido} - {self.cliente}'
    
    @property
    def is_dupla_densidade(self):
        """Verifica se o material é Dupla Densidade"""
        return 'dupla densidade' in self.tipo_material.nome.lower() if self.tipo_material else False
    
    def calcular_valores(self):
        """Calcula todos os valores do orçamento baseado nas regras da planilha"""
        try:
            from .calculadora import CalculadoraOrcamento
            calculadora = CalculadoraOrcamento(self)
            valores = calculadora.calcular()
            
            # Atualiza TODOS os valores calculados
            self.quantidade_unidades = int(valores['unidades'])
            self.milheiros = valores['milheiros']
            self.valor_unidade = valores['valor_unidade']
            self.valor_total = valores['valor_total']
            self.valor_metro = valores['valor_metro']
            self.valor_milheiro = valores['valor_milheiro']
            
            print(f"[OK] Valores calculados - Total: R$ {self.valor_total}, Unidades: {self.quantidade_unidades}")
        except Exception as e:
            print(f"[ERRO] Ao calcular valores: {e}")
            import traceback
            traceback.print_exc()
    
    def save(self, *args, **kwargs):
        # Calcula valores antes de salvar se já tem ID ou se é novo com dados
        # Verifica se tem os atributos necessários (evita erro com outros modelos)
        if hasattr(self, 'tipo_material_id') and hasattr(self, 'largura_mm') and hasattr(self, 'quantidade_metros'):
            if self.pk or (self.tipo_material_id and self.largura_mm and self.quantidade_metros):
                try:
                    self.calcular_valores()
                except Exception as e:
                    print(f"[ERRO] ao calcular valores: {e}")
                    pass  # Se falhar o cálculo, salva mesmo assim
        
        super().save(*args, **kwargs)


class CorOrcamento(models.Model):
    """
    Cores/Variantes de um orçamento
    Se for Dupla Densidade, permite 2 densidades
    """
    
    DENSIDADE_CHOICES = [
        ('1', '1ª Densidade'),
        ('2', '2ª Densidade'),
    ]
    
    COR_POSICAO_CHOICES = [
        ('Fd', 'Fundo (Fd)'),
        ('1', '1ª'),
        ('2', '2ª'),
        ('3', '3ª'),
        ('4', '4ª'),
        ('5', '5ª'),
        ('6', '6ª'),
        ('7', '7ª'),
    ]
    
    orcamento = models.ForeignKey(
        Orcamento,
        on_delete=models.CASCADE,
        related_name='cores'
    )
    
    # Posição da cor (Fd, 1ª, 2ª, etc)
    posicao = models.CharField(
        max_length=2,
        choices=COR_POSICAO_CHOICES,
        default='Fd'
    )
    
    # Densidade (1ª ou 2ª) - apenas para Dupla Densidade
    densidade = models.CharField(
        max_length=1,
        choices=DENSIDADE_CHOICES,
        default='1',
        help_text="1ª ou 2ª densidade (apenas para Dupla Densidade)"
    )
    
    # Código/Nome da cor
    codigo_cor = models.CharField(
        max_length=20,
        help_text="Ex: F01, T30, etc"
    )
    
    # Quantidade de unidades desta cor
    quantidade_unidades = models.IntegerField(
        validators=[MinValueValidator(1)],
        help_text="Quantas unidades desta cor"
    )
    
    # Quantidade de demais (opcional)
    quantidade_demais = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Coluna '+ Demais' (opcional)"
    )
    
    # Ordem de exibição
    ordem = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = 'Cor do Orçamento'
        verbose_name_plural = 'Cores do Orçamento'
        ordering = ['orcamento', 'densidade', 'ordem', 'posicao']
        unique_together = [['orcamento', 'posicao', 'densidade']]
    
    def __str__(self):
        densidade_str = f" ({self.densidade}ª densidade)" if self.densidade == '2' else ""
        return f'{self.orcamento.numero_pedido} - {self.get_posicao_display()}: {self.codigo_cor}{densidade_str}'
    
    @property
    def total_unidades(self):
        """Total de unidades (quantidade + demais)"""
        return self.quantidade_unidades + self.quantidade_demais


class Textura(models.Model):
    """Texturas disponíveis para as etiquetas"""
    codigo = models.CharField(max_length=20, unique=True)
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    ativo = models.BooleanField(default=True)
    ordem = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = 'Textura'
        verbose_name_plural = 'Texturas'
        ordering = ['ordem', 'codigo']
    
    def __str__(self):
        return f'{self.codigo} - {self.nome}'


class Fita(models.Model):
    """
    Tabela de Fatores para Fitas (Plan2 - Tabela FITAS)
    Relaciona a largura da fita com um fator de conversão/rendimento.
    """
    largura_mm = models.IntegerField(
        unique=True,
        validators=[MinValueValidator(1)],
        help_text="Largura da fita em mm"
    )
    fator = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        help_text="Fator de conversão/rendimento associado à largura"
    )
    
    class Meta:
        verbose_name = 'Fita (Fator)'
        verbose_name_plural = 'Fitas (Fatores)'
        ordering = ['largura_mm']

    def __str__(self):
        return f"{self.largura_mm}mm - Fator: {self.fator}"
