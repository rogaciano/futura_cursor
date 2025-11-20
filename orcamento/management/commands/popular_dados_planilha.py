from django.core.management.base import BaseCommand
from decimal import Decimal
from orcamento.models import (
    TipoMaterial, TipoCorte, TabelaPreco, CoeficienteFator,
    ValorGoma, ValorCorte, Configuracao, Textura
)


class Command(BaseCommand):
    help = 'Popula o banco de dados com os dados da planilha Excel'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Iniciando população do banco de dados...'))
        
        # 1. Criar Tipos de Material
        self.stdout.write('Criando tipos de material...')
        # Formato: (nome, codigo, ordem, batidas, batidas_2densidade)
        materiais = [
            ('Tafetá', 'TAFETA', 1, 20, 28),           # Baseado na planilha: J23=20, J25=28
            ('Sarja', 'SARJA', 2, 20, None),            # Assumindo padrão similar
            ('Alta Definição', 'ALTA_DEF', 3, 20, None),
            ('Dupla Densidade', 'DUPLA_DENS', 4, 20, 28),  # Material de dupla densidade
            ('Super Batidas', 'SUPER_BAT', 5, 30, None),   # Nome sugere mais batidas
            ('Canvas', 'CANVAS', 6, 20, None),
            ('Cetim', 'CETIM', 7, 20, None),
            ('SuperSoft', 'SUPERSOFT', 8, 20, None),
        ]
        
        for nome, codigo, ordem, batidas, batidas_2d in materiais:
            material, created = TipoMaterial.objects.update_or_create(
                codigo=codigo,
                defaults={
                    'nome': nome,
                    'ordem': ordem,
                    'batidas': batidas,
                    'batidas_2densidade': batidas_2d
                }
            )
            if created:
                self.stdout.write(f'  [+] Criado: {nome} (batidas: {batidas}{"/" + str(batidas_2d) if batidas_2d else ""})')
            else:
                self.stdout.write(f'  [~] Atualizado: {nome} (batidas: {batidas}{"/" + str(batidas_2d) if batidas_2d else ""})')
        
        # 2. Criar Tipos de Corte
        self.stdout.write('Criando tipos de corte...')
        cortes = [
            ('CORTE', 'CORTE', 5),
            ('DOBRA MEIO', 'DOBRA_MEIO', 10),
            ('DOBRA CANTOS', 'DOBRA_CANTOS', 13),
            ('CORTE NORMAL', 'CORTE_NORMAL', 12),
            ('ENVELOPE', 'ENVELOPE', 8),
            ('DOBRA DESCENTRALIZADA', 'DOBRA_DESC', 22),
            ('MEIO CORTE', 'MEIO_CORTE', 11),
            ('SAQUINHO', 'SAQUINHO', 9),
            ('CORTE ESPECIAL', 'CORTE_ESP', 15),
        ]
        
        for nome, codigo, codigo_calc in cortes:
            TipoCorte.objects.get_or_create(
                codigo=codigo,
                defaults={'nome': nome, 'codigo_calc': codigo_calc}
            )
        
        # 3. Criar Tabela de Preços (baseado na planilha Plan2)
        self.stdout.write('Criando tabela de preços...')
        metragens = [300, 500, 1000, 2500, 5000, 10000, 15000, 30000]
        
        # Preços exemplo para Tafetá
        precos_tafeta = [20.40, 15.69, 10.44, 10.11, 9.35, 8.39, 8.04, 7.72]
        tafeta = TipoMaterial.objects.get(codigo='TAFETA')
        for metragem, preco in zip(metragens, precos_tafeta):
            TabelaPreco.objects.get_or_create(
                metragem=metragem,
                tipo_material=tafeta,
                defaults={'preco_metro': Decimal(str(preco))}
            )
        
        # Preços exemplo para Sarja
        precos_sarja = [22.50, 17.29, 11.48, 11.12, 10.29, 9.22, 8.84, 8.48]
        sarja = TipoMaterial.objects.get(codigo='SARJA')
        for metragem, preco in zip(metragens, precos_sarja):
            TabelaPreco.objects.get_or_create(
                metragem=metragem,
                tipo_material=sarja,
                defaults={'preco_metro': Decimal(str(preco))}
            )
        
        # Preços exemplo para Alta Definição
        precos_alta_def = [26.84, 20.64, 14.36, 13.21, 12.58, 11.89, 11.35, 10.89]
        alta_def = TipoMaterial.objects.get(codigo='ALTA_DEF')
        for metragem, preco in zip(metragens, precos_alta_def):
            TabelaPreco.objects.get_or_create(
                metragem=metragem,
                tipo_material=alta_def,
                defaults={'preco_metro': Decimal(str(preco))}
            )
        
        # 4. Criar Coeficientes Fator (exemplos baseados na planilha)
        self.stdout.write('Criando coeficientes fator...')
        larguras = [10, 12, 15, 18, 20, 21, 24, 28, 30, 33, 40, 50, 67, 100]
        
        # Coeficientes para Tafetá
        coefs_tafeta = [0.97, 0.97, 0.97, 0.97, 0.97, 0.97, 0.97, 0.97, 0.97, 0.97, 0.97, 0.97, 0.97, 0.97]
        corte = TipoCorte.objects.get(codigo='CORTE')
        for largura, coef in zip(larguras, coefs_tafeta):
            CoeficienteFator.objects.get_or_create(
                largura=largura,
                tipo_material=tafeta,
                codigo_corte=corte,
                defaults={'coeficiente': Decimal(str(coef))}
            )
        
        # 5. Criar Valores de Goma (baseado na planilha)
        self.stdout.write('Criando valores de goma...')
        larguras_goma = [10, 12, 15, 18, 20, 21, 24, 28, 30, 33, 40, 50, 67, 100]
        gomas_fino = [0.029, 0.035, 0.043, 0.051, 0.058, 0.065, 0.073, 0.085, 0.1, 0.1, 0.116, 0.145, 0.194, 0.29]
        gomas_grosso = [0.052, 0.062, 0.078, 0.089, 0.1, 0.107, 0.11, 0.128, 0.136, 0.136, 0.176, 0.22, 0.295, 0.44]
        gomas_termo = [0.2, 0.2, 0.25, 0.3, 0.3, 0.3, 0.4, 0.45, 0.5, 0.5, 0.55, 0.7, 0.95, 1.4]
        
        for largura, fino, grosso, termo in zip(larguras_goma, gomas_fino, gomas_grosso, gomas_termo):
            ValorGoma.objects.get_or_create(
                largura=largura,
                defaults={
                    'goma_fino': Decimal(str(fino)),
                    'goma_grosso': Decimal(str(grosso)),
                    'termocolante': Decimal(str(termo))
                }
            )
        
        # 6. Criar Valores de Corte (Canvas e Cetim)
        self.stdout.write('Criando valores de corte especial...')
        for largura in larguras_goma:
            ValorCorte.objects.get_or_create(
                largura=largura,
                defaults={
                    'canvas': Decimal('0.189'),
                    'cetim': Decimal('0.087')
                }
            )
        
        # 7. Criar Configurações
        self.stdout.write('Criando configurações...')
        configs = [
            ('perc_ultrassonico', '1.15', 'Percentual de aumento para corte ultrassônico', 'decimal'),
            ('perc_aumento_geral', '1.00', 'Percentual de aumento geral', 'decimal'),
        ]
        
        for chave, valor, descricao, tipo_dado in configs:
            Configuracao.objects.get_or_create(
                chave=chave,
                defaults={
                    'valor': valor,
                    'descricao': descricao,
                    'tipo_dado': tipo_dado
                }
            )
        
        # 8. Criar Texturas (baseado na planilha)
        self.stdout.write('Criando texturas...')
        texturas = [
            ('1', 'PIMENTAS'),
            ('2', 'FOLHAS'),
            ('3', 'HIBISCO'),
            ('4', 'CAFÉ'),
            ('5', 'FLORES'),
            ('6', 'PEDRAS'),
            ('7', 'XADREZ'),
            ('8', 'LIG8'),
            ('9', 'LIG10'),
            ('10', 'LIG16'),
            ('11', 'SARJADO'),
            ('12', 'ZIG ZAG'),
            ('13', 'ALMOFADADO'),
            ('14', 'ALMOFADADO P'),
            ('15', 'DIAMANTADO P'),
            ('16', 'LADRILHO'),
            ('17', 'MOSAICO'),
            ('18', 'INDIANO'),
            ('19', 'CANELADO'),
            ('20', 'ONDAS'),
            ('21', 'CASULO'),
            ('22', 'CIRCULOS'),
            ('23', 'DIAMANTADO'),
            ('24', 'DEGRAUS'),
            ('25', 'DUNAS'),
            ('26', 'ENGRENAGEM'),
            ('27', 'JEANS'),
            ('28', 'SAFIRA'),
            ('29', 'CORAÇÃO'),
            ('30', '3D'),
        ]
        
        for ordem, (codigo, nome) in enumerate(texturas, 1):
            Textura.objects.get_or_create(
                codigo=codigo,
                defaults={'nome': nome, 'ordem': ordem}
            )
        
        self.stdout.write(self.style.SUCCESS('Banco de dados populado com sucesso!'))
        self.stdout.write(self.style.SUCCESS(f'  - {TipoMaterial.objects.count()} tipos de material'))
        self.stdout.write(self.style.SUCCESS(f'  - {TipoCorte.objects.count()} tipos de corte'))
        self.stdout.write(self.style.SUCCESS(f'  - {TabelaPreco.objects.count()} precos cadastrados'))
        self.stdout.write(self.style.SUCCESS(f'  - {CoeficienteFator.objects.count()} coeficientes'))
        self.stdout.write(self.style.SUCCESS(f'  - {ValorGoma.objects.count()} valores de goma'))
        self.stdout.write(self.style.SUCCESS(f'  - {ValorCorte.objects.count()} valores de corte'))
        self.stdout.write(self.style.SUCCESS(f'  - {Configuracao.objects.count()} configuracoes'))
        self.stdout.write(self.style.SUCCESS(f'  - {Textura.objects.count()} texturas'))

