# 📚 Exemplos de Uso do Sistema

## Exemplo 1: Orçamento Simples - Etiqueta Tafetá

### Dados do Pedido
- **Cliente**: Confecções Silva Ltda
- **Tipo**: Indústria Novo
- **Material**: Tafetá
- **Dimensões**: 30mm x 50mm
- **Quantidade**: 1000 metros / 5000 unidades
- **Corte**: Corte Normal
- **Sem goma, sem ultrassônico**

### Cálculo Realizado
```
1. Preço base (1000m, Tafetá): R$ 10,44/m
2. Coeficiente fator (30mm, Tafetá): 0.97
3. Valor calculado: 10.44 × 0.97 = R$ 10,13/m
4. Valor milheiro: R$ 506,50
5. Valor unidade: R$ 0,50650
6. Valor total (5000 un): R$ 2.532,50
```

## Exemplo 2: Orçamento com Goma - Etiqueta Alta Definição

### Dados do Pedido
- **Cliente**: Moda Fashion Store
- **Tipo**: Comércio Novo
- **Material**: Alta Definição
- **Dimensões**: 50mm x 80mm
- **Quantidade**: 5000 metros / 10000 unidades
- **Corte**: Dobra Meio
- **Goma**: Termocolante
- **Sem ultrassônico**

### Cálculo Realizado
```
1. Preço base (5000m, Alta Def): R$ 12,58/m
2. Coeficiente fator (50mm, Alta Def): 0.71
3. Valor goma termocolante (50mm): R$ 0,70
4. Valor calculado: (12.58 × 0.71) + 0.70 = R$ 9,63/m
5. Fator cliente (Comércio Novo): 1.1
6. Valor ajustado: 9.63 × 1.1 = R$ 10,59/m
7. Valor milheiro: R$ 847,20
8. Valor unidade: R$ 0,84720
9. Valor total (10000 un): R$ 8.472,00
```

## Exemplo 3: Orçamento Completo - Etiqueta Canvas com Ultrassônico

### Dados do Pedido
- **Cliente**: Premium Brands International
- **Tipo**: Indústria Antigo
- **Material**: Canvas
- **Dimensões**: 67mm x 120mm
- **Quantidade**: 15000 metros / 25000 unidades
- **Corte**: Envelope
- **Goma**: Grosso
- **Corte Ultrassônico**: Sim

### Cálculo Realizado
```
1. Preço base (15000m, Canvas): R$ 8,04/m
2. Coeficiente fator (67mm, Canvas): 0.51
3. Valor goma grosso (67mm): R$ 0,295
4. Valor corte especial Canvas (67mm): R$ 0,189
5. Subtotal: (8.04 × 0.51) + 0.295 + 0.189 = R$ 4,58/m
6. Percentual ultrassônico (15%): 4.58 × 1.15 = R$ 5,27/m
7. Fator cliente (Indústria Antigo): 0.95
8. Valor ajustado: 5.27 × 0.95 = R$ 5,01/m
9. Valor milheiro: R$ 627,50
10. Valor unidade: R$ 0,62750
11. Valor total (25000 un): R$ 15.687,50
```

## Exemplo 4: Orçamento Dupla Densidade

### Dados do Pedido
- **Cliente**: Sports Wear Brasil
- **Tipo**: Comércio Antigo
- **Material**: Dupla Densidade
- **Dimensões**: 40mm x 70mm
- **Quantidade**: 2500 metros / 8000 unidades
- **Corte**: Corte Especial
- **Goma**: Fino
- **Sem ultrassônico**

### Nota Especial
> **Dupla Densidade**: A largura é automaticamente dividida por 2 nos cálculos!
> Largura informada: 40mm → Largura de cálculo: 20mm

### Cálculo Realizado
```
1. Preço base (2500m, Dupla Dens): R$ 10,11/m
2. Largura real para cálculo: 40mm ÷ 2 = 20mm
3. Coeficiente fator (20mm, Dupla Dens): 0.66
4. Valor goma fino (20mm): R$ 0,058
5. Valor calculado: (10.11 × 0.66) + 0.058 = R$ 6,73/m
6. Fator cliente (Comércio Antigo): 1.05
7. Valor ajustado: 6.73 × 1.05 = R$ 7,07/m
8. Valor milheiro: R$ 883,75
9. Valor unidade: R$ 0,88375
10. Valor total (8000 un): R$ 7.070,00
```

## Exemplo 5: Comparação de Tipos de Cliente

### Mesmo Pedido, Tipos Diferentes

**Especificações Base**:
- Material: Sarja
- Dimensões: 30mm x 60mm
- Quantidade: 5000 metros / 15000 unidades
- Corte: Dobra Cantos
- Sem goma, sem ultrassônico

### Cálculos por Tipo de Cliente

#### Indústria Novo (Fator: 1.0)
```
Valor base: R$ 10,29/m
Valor total: R$ 15.435,00
```

#### Indústria Antigo (Fator: 0.95)
```
Valor base: R$ 10,29/m
Valor com desconto: R$ 9,78/m
Valor total: R$ 14.670,00
Economia: R$ 765,00 (5%)
```

#### Comércio Novo (Fator: 1.1)
```
Valor base: R$ 10,29/m
Valor com acréscimo: R$ 11,32/m
Valor total: R$ 16.980,00
Diferença: +R$ 1.545,00 (10%)
```

#### Comércio Antigo (Fator: 1.05)
```
Valor base: R$ 10,29/m
Valor com acréscimo: R$ 10,80/m
Valor total: R$ 16.200,00
Diferença: +R$ 765,00 (5%)
```

## Exemplo 6: Impacto da Metragem no Preço

### Mesmo Produto, Quantidades Diferentes

**Especificações**:
- Material: Alta Definição
- Dimensões: 50mm x 70mm
- Corte: Corte Normal
- Sem goma, sem ultrassônico

### Tabela Comparativa

| Quantidade (metros) | Preço Base (m) | Valor Milheiro | Valor 10.000 un |
|---------------------|----------------|----------------|-----------------|
| 300                 | R$ 26,84       | R$ 1.908,00    | R$ 19.080,00    |
| 500                 | R$ 20,64       | R$ 1.466,00    | R$ 14.660,00    |
| 1.000               | R$ 14,36       | R$ 1.020,00    | R$ 10.200,00    |
| 2.500               | R$ 13,21       | R$ 938,00      | R$ 9.380,00     |
| 5.000               | R$ 12,58       | R$ 894,00      | R$ 8.940,00     |
| 10.000              | R$ 11,89       | R$ 845,00      | R$ 8.450,00     |
| 15.000              | R$ 11,35       | R$ 807,00      | R$ 8.070,00     |
| 30.000              | R$ 10,89       | R$ 774,00      | R$ 7.740,00     |

**Economia ao aumentar volume**:
- De 300m para 30.000m: **59% de economia!**
- De 1.000m para 10.000m: **17% de economia**

## Dicas para Otimizar Preços

### 1. Volume é Fundamental
- Sempre que possível, consolide pedidos
- Quanto maior a metragem, menor o preço unitário
- Considere fazer estoque de itens recorrentes

### 2. Escolha do Material
- Tafetá: Mais econômico, boa qualidade
- Alta Definição: Melhor qualidade, preço premium
- Canvas/Cetim: Especiais, com valores adicionais

### 3. Opções Adicionais
- **Goma**: Adiciona R$ 0,03 a R$ 1,40 por metro dependendo do tipo
- **Ultrassônico**: Acrescenta 15% no valor final
- **Tipo de Corte**: Alguns cortes têm coeficientes diferentes

### 4. Tipo de Cliente
- Negociar status de "Antigo" economiza 5%
- Indústrias têm melhores preços que comércios
- Considere volume anual para negociação

## Casos de Uso Reais

### Caso 1: Confecção de Roupas Infantis
```
- 5 tipos diferentes de etiquetas
- Volume total: 50.000 unidades/ano
- Material preferido: Tafetá e Sarja
- Estratégia: Pedidos consolidados mensais de 4.000+ unidades
- Resultado: Economia de 12% vs pedidos semanais
```

### Caso 2: Marca de Luxo
```
- Etiquetas premium com Canvas
- Volume: 15.000 unidades/trimestre
- Material: Canvas + Cetim
- Opções: Goma termocolante + Ultrassônico
- Foco: Qualidade > Preço
```

### Caso 3: Atacadista de Roupas
```
- Grande variedade de tamanhos
- Volume: 100.000+ unidades/ano
- Material: Mix de Tafetá, Sarja e Alta Definição
- Estratégia: Pedidos consolidados de 10.000m+
- Resultado: Melhor preço de mercado
```

## Calculadora Rápida

### Estimativa Aproximada
Para uma **estimativa rápida** sem entrar no sistema:

```
Valor aproximado = (Preço base × 0.7) × Quantidade
```

Exemplo:
- Tafetá, 1000m, 5000 unidades
- Preço base: R$ 10,44/m
- Estimativa: (10.44 × 0.7) × 5000 = R$ 3.654,00
- Valor real no sistema: ~R$ 3.200,00

> **Nota**: Use o sistema para valores precisos!

---

Para mais informações, consulte o **README.md** ou acesse o **sistema** para cálculos exatos.

