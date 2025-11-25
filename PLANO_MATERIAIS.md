# Plano de Implementação: Tabela de Materiais (Acabamentos)

Com base na sua correção, entendi que "Materiais" (O25) se refere aos acabamentos/insumos extras e não aos tipos de tecido.

## 1. Novos Modelos
Criarei dois modelos para substituir a lógica atual de `ValorGoma` e `ValorCorte`:

### `Acabamento`
Lista os materiais disponíveis conforme indicado:
- Goma F
- Goma G
- Cola Fria
- Termocolante
- Interce Fino
- Interce Grosso
- Overloque + interce

### `PrecoAcabamento`
Armazena o preço por milímetro de largura para cada acabamento (baseado na Plan2).
- Campos: `largura_mm`, `acabamento`, `preco`.

## 2. Alterações no Orçamento
- Remover campos `tem_goma` e `tipo_goma`.
- Adicionar campo `acabamento` (ForeignKey para `Acabamento`).
- Manter `tem_ultrassonico` separado (pois não consta na lista de materiais fornecida).

## 3. Migração de Dados
- Vou extrair os preços das colunas F, G, colafria, termo, fino, grosso da Plan2.
- **Atenção:** Para "Overloque + interce", como não encontrei coluna correspondente na planilha, deixarei com valor R$ 0,00 inicialmente, editável pelo painel administrativo.

## 4. Atualização de Cálculos
- A calculadora buscará o preço na tabela `PrecoAcabamento` baseada na largura e acabamento selecionado.

Posso prosseguir com este plano?
