#!/usr/bin/env python
"""
Script de teste rápido do sistema de orçamentos
Execute: python teste_sistema.py
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from orcamento.models import (
    TipoMaterial, TipoCorte, TabelaPreco, 
    CoeficienteFator, ValorGoma, Orcamento
)
from decimal import Decimal


def testar_banco_dados():
    """Testa se o banco de dados está populado"""
    print("\n" + "="*60)
    print("TESTE 1: Verificando Banco de Dados")
    print("="*60)
    
    testes = [
        ("Tipos de Material", TipoMaterial.objects.count(), 8),
        ("Tipos de Corte", TipoCorte.objects.count(), 9),
        ("Preços Cadastrados", TabelaPreco.objects.count(), 24),
        ("Coeficientes", CoeficienteFator.objects.count(), 14),
        ("Valores de Goma", ValorGoma.objects.count(), 14),
    ]
    
    todos_ok = True
    for nome, atual, esperado in testes:
        status = "[OK]" if atual >= esperado else "[ERRO]"
        print(f"{status} {nome}: {atual} (esperado: >= {esperado})")
        if atual < esperado:
            todos_ok = False
    
    return todos_ok


def testar_calculo_simples():
    """Testa um cálculo simples"""
    print("\n" + "="*60)
    print("TESTE 2: Cálculo Simples")
    print("="*60)
    
    try:
        # Criar orçamento de teste
        tafeta = TipoMaterial.objects.get(codigo='TAFETA')
        corte = TipoCorte.objects.get(codigo='CORTE')
        
        orcamento = Orcamento(
            cliente="Cliente Teste",
            tipo_cliente="comercio_novo",
            tipo_material=tafeta,
            largura_mm=30,
            comprimento_mm=50,
            quantidade_metros=1000,
            quantidade_unidades=5000,
            tipo_corte=corte,
        )
        
        # Calcular valores
        orcamento.calcular_valores()
        
        print(f"Cliente: {orcamento.cliente}")
        print(f"Material: {orcamento.tipo_material.nome}")
        print(f"Dimensões: {orcamento.largura_mm}mm x {orcamento.comprimento_mm}mm")
        print(f"Quantidade: {orcamento.quantidade_metros}m / {orcamento.quantidade_unidades} un")
        print(f"\nResultados:")
        print(f"  Valor por Metro: R$ {orcamento.valor_metro}")
        print(f"  Valor Milheiro: R$ {orcamento.valor_milheiro}")
        print(f"  Valor Unidade: R$ {orcamento.valor_unidade}")
        print(f"  Valor Total: R$ {orcamento.valor_total}")
        
        # Verificar se os valores foram calculados
        if orcamento.valor_total > 0:
            print("\n[OK] Calculo realizado com sucesso!")
            return True
        else:
            print("\n[ERRO] Erro: Valores zerados")
            return False
            
    except Exception as e:
        print(f"\n[ERRO] Erro no calculo: {str(e)}")
        return False


def testar_materiais():
    """Lista os materiais disponíveis"""
    print("\n" + "="*60)
    print("TESTE 3: Materiais Disponíveis")
    print("="*60)
    
    materiais = TipoMaterial.objects.filter(ativo=True).order_by('ordem')
    
    for i, material in enumerate(materiais, 1):
        print(f"{i}. {material.nome} ({material.codigo})")
    
    return materiais.count() > 0


def testar_precos():
    """Testa a tabela de preços"""
    print("\n" + "="*60)
    print("TESTE 4: Tabela de Preços (Tafetá)")
    print("="*60)
    
    try:
        tafeta = TipoMaterial.objects.get(codigo='TAFETA')
        precos = TabelaPreco.objects.filter(tipo_material=tafeta).order_by('metragem')
        
        print(f"\n{'Metragem':<12} {'Preço/Metro':>12}")
        print("-" * 25)
        for preco in precos:
            print(f"{preco.metragem:<12} R$ {preco.preco_metro:>9.2f}")
        
        return precos.count() > 0
        
    except Exception as e:
        print(f"[ERRO] Erro: {str(e)}")
        return False


def main():
    """Executa todos os testes"""
    print("\n" + "="*60)
    print("SISTEMA DE ORÇAMENTOS - TESTES AUTOMÁTICOS")
    print("="*60)
    
    resultados = []
    
    # Executar testes
    resultados.append(("Banco de Dados", testar_banco_dados()))
    resultados.append(("Cálculo Simples", testar_calculo_simples()))
    resultados.append(("Materiais", testar_materiais()))
    resultados.append(("Preços", testar_precos()))
    
    # Resumo
    print("\n" + "="*60)
    print("RESUMO DOS TESTES")
    print("="*60)
    
    total = len(resultados)
    aprovados = sum(1 for _, ok in resultados if ok)
    
    for teste, ok in resultados:
        status = "[OK] PASSOU" if ok else "[ERRO] FALHOU"
        print(f"{teste:.<40} {status}")
    
    print("\n" + "="*60)
    print(f"Total: {aprovados}/{total} testes aprovados")
    print("="*60)
    
    if aprovados == total:
        print("\n[SUCCESS] TODOS OS TESTES PASSARAM!")
        print("Sistema esta pronto para uso!")
        print("\nProximos passos:")
        print("1. python manage.py createsuperuser")
        print("2. python manage.py runserver")
        print("3. Acesse: http://127.0.0.1:8000/")
    else:
        print("\n[WARNING] Alguns testes falharam")
        print("Verifique as mensagens de erro acima")
    
    print("\n")


if __name__ == "__main__":
    main()

