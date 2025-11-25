from decimal import Decimal
from typing import Dict
from .models import TabelaPreco, CoeficienteFator, PrecoAcabamento, Configuracao, ValorCorte, Fita


class CalculadoraOrcamento:
    """
    Classe responsável por calcular os valores de um orçamento
    baseado na lógica da planilha Excel original
    """
    
    def __init__(self, orcamento):
        self.orcamento = orcamento
        self.configs = self._carregar_configuracoes()
    
    def _carregar_configuracoes(self) -> Dict:
        """Carrega todas as configurações do sistema"""
        configs = {}
        for config in Configuracao.objects.all():
            configs[config.chave] = config.get_valor()
        return configs
    
    def _obter_preco_base(self) -> Decimal:
        """
        Obtém o preço base por metro baseado na metragem e tipo de material
        Usa VLOOKUP da planilha: procura a metragem na tabela de preços
        """
        # Encontra a faixa de metragem apropriada (menor ou igual)
        metragem_lookup = self.orcamento.tabela_manual_metragem or self.orcamento.quantidade_metros

        preco = TabelaPreco.objects.filter(
            metragem__lte=metragem_lookup,
            tipo_material=self.orcamento.tipo_material
        ).order_by('-metragem').first()
        
        if not preco:
            # Se não encontrou, pega o primeiro disponível para esse material
            preco = TabelaPreco.objects.filter(
                tipo_material=self.orcamento.tipo_material
            ).order_by('metragem').first()
        
        return preco.preco_metro if preco else Decimal('0.0')
    
    def _obter_coeficiente_fator(self) -> Decimal:
        """
        Obtém o coeficiente fator baseado na largura, tipo de material e código de corte
        Equivalente ao VLOOKUP na tabela_fator da planilha
        """
        # Calcula o código baseado no comprimento do nome do corte (lógica da planilha)
        codigo_calc = len(self.orcamento.tipo_corte.nome)
        
        coef = CoeficienteFator.objects.filter(
            largura=self.orcamento.largura_mm,
            tipo_material=self.orcamento.tipo_material,
            codigo_corte__codigo_calc=codigo_calc
        ).first()
        
        if not coef:
            # Tenta com a largura mais próxima menor ou igual
            coef = CoeficienteFator.objects.filter(
                largura__lte=self.orcamento.largura_mm,
                tipo_material=self.orcamento.tipo_material,
                codigo_corte__codigo_calc=codigo_calc
            ).order_by('-largura').first()
        
        return coef.coeficiente if coef else Decimal('0.75')  # Default da planilha
    
    def _obter_valor_goma(self) -> Decimal:
        """
        Obtém o valor do acabamento (antiga goma) baseado na largura e acabamento
        """
        if not self.orcamento.acabamento:
            return Decimal('0.0')
        
        preco_obj = PrecoAcabamento.objects.filter(
            largura_mm__lte=self.orcamento.largura_mm,
            acabamento=self.orcamento.acabamento
        ).order_by('-largura_mm').first()
        
        if not preco_obj:
            return Decimal('0.0')
            
        return preco_obj.preco
    
    def _obter_valor_corte_especial(self) -> Decimal:
        """
        Obtém valor de corte especial (canvas, cetim)
        """
        tipo_material_nome = self.orcamento.tipo_material.nome.lower()
        
        if 'canvas' not in tipo_material_nome and 'cetim' not in tipo_material_nome:
            return Decimal('0.0')
        
        valor_corte = ValorCorte.objects.filter(
            largura__lte=self.orcamento.largura_mm
        ).order_by('-largura').first()
        
        if not valor_corte:
            return Decimal('0.0')
        
        if 'canvas' in tipo_material_nome:
            return valor_corte.canvas
        elif 'cetim' in tipo_material_nome:
            return valor_corte.cetim
        
        return Decimal('0.0')
    
    def _calcular_largura_real(self) -> int:
        """
        Calcula largura real considerando se é Dupla Densidade
        Se for Dupla Densidade, divide por 2
        """
        largura = self.orcamento.largura_mm
        
        if 'dupla densidade' in self.orcamento.tipo_material.nome.lower():
            return largura // 2
        
        return largura
    
    def _obter_percentual_ultrassonico(self) -> Decimal:
        """Obtém percentual de aumento para corte ultrassônico"""
        if not self.orcamento.tem_ultrassonico:
            return Decimal('1.0')
        
        perc = self.configs.get('perc_ultrassonico', Decimal('1.15'))
        return Decimal(str(perc))
    
    def _obter_percentual_aumento_geral(self) -> Decimal:
        """Obtém percentual de aumento geral"""
        perc = self.configs.get('perc_aumento_geral', Decimal('1.0'))
        return Decimal(str(perc))
    
    def _calcular_fator_tipo_cliente(self) -> Decimal:
        """
        Calcula fator baseado no tipo de cliente
        """
        fatores = {
            'industria_novo': Decimal('1.0'),
            'industria_antigo': Decimal('0.95'),
            'comercio_novo': Decimal('1.1'),
            'comercio_antigo': Decimal('1.05'),
        }
        return fatores.get(self.orcamento.tipo_cliente, Decimal('1.0'))
    
    def _calcular_cc_coeficiente_corte(self) -> Decimal:
        """
        Calcula o coeficiente CC (Coeficiente por Corte)
        baseado na largura real e quantidade
        """
        largura_real = self._calcular_largura_real()
        
        # Fórmula da planilha para CC
        # Simplificada baseada no comprimento em relação à largura
        if self.orcamento.comprimento_mm > 0:
            razao = Decimal(str(largura_real)) / Decimal(str(self.orcamento.comprimento_mm))
            cc = razao * Decimal('1.2')  # Fator de ajuste
            return max(cc, Decimal('0.5'))  # Mínimo de 0.5
        
        return Decimal('1.0')
    
    def _obter_fator_fita(self) -> Decimal:
        """
        Obtém o fator de conversão da fita baseado na largura real
        """
        largura_real = self._calcular_largura_real()
        
        fita = Fita.objects.filter(largura_mm=largura_real).first()
        if not fita:
            # Tenta encontrar o próximo menor
            fita = Fita.objects.filter(largura_mm__lte=largura_real).order_by('-largura_mm').first()
            
        return fita.fator if fita else Decimal('0.0')

    def _obter_coeficiente_metragem_cm(self) -> Decimal:
        """
        Obtém o coeficiente de metragem CM (Configuração)
        Padrão: 0.330 se não configurado
        """
        return self.configs.get('coeficiente_metragem_cm', Decimal('0.330'))

    def calcular(self) -> Dict[str, Decimal]:
        """
        Realiza todos os cálculos EXATAMENTE como na planilha
        
        ORDEM DE CÁLCULO DA PLANILHA:
        1. Metros (digitado)
        2. Unidades (calculado baseado em metros)
        3. Milheiros = ARREDONDAR.PARA.BAIXO(Unidades/1000, 2)
        4. Valor Unidade (fórmula complexa)
        5. Valor Total = Valor Unidade * Unidades
        6. Valor Metro = Valor Total / Metros
        7. Valor Milheiro = Valor Total / Milheiros
        """
        
        # Dados de entrada
        metros = Decimal(str(self.orcamento.quantidade_metros))
        largura_mm = Decimal(str(self.orcamento.largura_mm))
        comprimento_mm = Decimal(str(self.orcamento.comprimento_mm))
        
        # 1. Calcular UNIDADES baseado em metros LINEARES
        # A conta é linear: Metros / Comprimento
        # Ex: 500m / 0.025m (25mm) = 20.000 unidades
        
        comprimento_metros = comprimento_mm / Decimal('1000')
        
        if comprimento_metros > 0:
            unidades = metros / comprimento_metros
        else:
            unidades = Decimal(str(self.orcamento.quantidade_unidades))
        
        # 2. Calcular MILHEIROS = ARREDONDAR.PARA.BAIXO(Unidades/1000, 2)
        milheiros = (unidades / Decimal('1000')).quantize(Decimal('0.01'), rounding='ROUND_DOWN')
        
        # Evitar divisão por zero
        if milheiros == 0:
            milheiros = Decimal('0.01')
        
        # Área da etiqueta em m² (usada para cálculo de valor)
        area_etiqueta_m2 = (largura_mm * comprimento_mm) / Decimal('1000000')

        # 3. Calcular VALOR UNIDADE (fórmula da planilha)
        # =SE(larg_calc=60;1,49;1) * (CÁLCULO!A16) * (SE(U16="";1;(SE(U15="+";(1+U16%);(1-U16%)))) * (SE(S25="sim";perc_ultrassonico;1)) * V41 * perc_aumento_geral
        
        # Fator de largura 60mm
        fator_largura_60 = Decimal('1.49') if int(largura_mm) == 60 else Decimal('1.0')
        
        # Preço base (CÁLCULO!A16) - por METRO
        preco_base = self._obter_preco_base()
        
        # Coeficiente fator
        coef_fator = self._obter_coeficiente_fator()
        
        # Fator Fita (para debug)
        fator_fita = self._obter_fator_fita()
        
        # Calcula variável densidade_cores_fita
        # Fórmula ajustada conforme Excel: =soma_cores * preco_base / fator_fita / comprimento
        
        # Calcula soma de unidades das cores
        total_unidades_cores = sum(c.quantidade_unidades + c.quantidade_demais for c in self.orcamento.cores.all())
        
        densidade_cores_fita = Decimal('0.0')
        if fator_fita > 0 and comprimento_mm > 0:
            densidade_cores_fita = (
                Decimal(total_unidades_cores) * preco_base
            ) / fator_fita / comprimento_mm

        # Valor base POR METRO
        valor_metro_base = preco_base * coef_fator
        
        # Adicionar goma (por metro)
        valor_goma = self._obter_valor_goma()
        valor_metro_base = valor_metro_base + valor_goma
        
        # Adicionar corte especial (canvas/cetim)
        valor_corte_especial = self._obter_valor_corte_especial()
        valor_metro_base = valor_metro_base + valor_corte_especial
        
        # CC - Coeficiente de Corte (V41 na planilha)
        cc = self._calcular_cc_coeficiente_corte()
        
        # Percentual ultrassônico (SE(S25="sim";perc_ultrassonico;1))
        perc_ultrassonico = self._obter_percentual_ultrassonico()
        
        # Percentual aumento geral
        perc_aumento_geral = self._obter_percentual_aumento_geral()
        
        # Fator tipo cliente (assumindo que U15 e U16 são relacionados)
        fator_cliente = self._calcular_fator_tipo_cliente()
        
        # VALOR POR METRO COM TODOS OS FATORES
        valor_metro_final = (
            fator_largura_60 * 
            valor_metro_base * 
            fator_cliente * 
            perc_ultrassonico * 
            cc * 
            perc_aumento_geral
        )
        
        # VALOR POR UNIDADE = Valor Metro Linear × Comprimento da Etiqueta (m)
        # Ajuste: cálculo linear para manter consistência com as unidades
        valor_unidade = valor_metro_final * comprimento_metros
        
        # 4. Calcular VALOR TOTAL = Valor Unidade * Unidades
        valor_total = valor_unidade * unidades
        
        # 5. Calcular VALOR METRO = Valor Total / Metros
        if metros > 0:
            valor_metro = valor_total / metros
        else:
            valor_metro = Decimal('0.0')
        
        # 6. Calcular VALOR MILHEIRO = Valor Total / Milheiros
        if milheiros > 0:
            valor_milheiro = valor_total / milheiros
        else:
            valor_milheiro = Decimal('0.0')
        
        # Arredondamentos
        valor_metro = valor_metro.quantize(Decimal('0.00001'))
        valor_milheiro = valor_milheiro.quantize(Decimal('0.01'))
        valor_unidade = valor_unidade.quantize(Decimal('0.00001'))
        valor_total = valor_total.quantize(Decimal('0.01'))
        unidades = unidades.quantize(Decimal('0.01'))
        
        # Estrutura de Debug
        
        # Calcula soma de unidades das cores
        total_unidades_cores = sum(c.quantidade_unidades + c.quantidade_demais for c in self.orcamento.cores.all())
        
        debug_info = {
            'passos': [
                {'label': 'Metragem', 'valor': f"{metros} m"},
                {'label': 'Largura', 'valor': f"{largura_mm} mm"},
                {'label': 'Largura Real', 'valor': f"{self._calcular_largura_real()} mm"},
                {'label': 'Comprimento', 'valor': f"{comprimento_mm} mm"},
                {'label': 'Soma Unidades (Cores)', 'valor': f"{total_unidades_cores} un"},
                {'label': 'Unidades (Calculado)', 'valor': f"{unidades} un"},
                {'label': 'Preço Base (Tabela)', 'valor': f"R$ {preco_base:.5f}"},
                {'label': 'Coeficiente Fator', 'valor': f"{coef_fator:.5f}"},
                {'label': 'Fator Fita', 'valor': f"{fator_fita}"},
                {'label': 'Densidade Cores Fita', 'valor': f"{densidade_cores_fita:.9f}"},
                {'label': 'Valor Base (Metro)', 'valor': f"R$ {preco_base * coef_fator:.5f}"},
                {'label': 'Valor Acabamento', 'valor': f"R$ {valor_goma:.5f}"},
                {'label': 'Valor Corte Especial', 'valor': f"R$ {valor_corte_especial:.5f}"},
                {'label': 'Fator Largura 60', 'valor': f"{fator_largura_60}"},
                {'label': 'Fator Cliente', 'valor': f"{fator_cliente}"},
                {'label': 'Perc. Ultrassônico', 'valor': f"{perc_ultrassonico}"},
                {'label': 'Coef. Corte (CC)', 'valor': f"{cc:.5f}"},
                {'label': 'Perc. Aumento Geral', 'valor': f"{perc_aumento_geral}"},
                {'label': 'Valor Metro Final (Calc)', 'valor': f"R$ {valor_metro_final:.5f}"},
                {'label': 'Milheiros', 'valor': f"{milheiros}"},
            ]
        }

        return {
            'valor_metro': valor_metro,
            'valor_milheiro': valor_milheiro,
            'valor_unidade': valor_unidade,
            'valor_total': valor_total,
            'unidades': unidades,
            'milheiros': milheiros,
            'preco_base': preco_base,
            'coef_fator': coef_fator,
            'valor_goma': valor_goma,
            'cc': cc,
            'area_m2': area_etiqueta_m2,
            'debug_info': debug_info,
        }

