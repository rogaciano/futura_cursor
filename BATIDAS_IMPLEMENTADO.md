# ✅ Campo "Batidas" Implementado

## O que foi feito:

### 1. **Modelo de Dados** ✅
Adicionados campos ao modelo `TipoMaterial`:
- `batidas`: Número de batidas para 1ª densidade ou densidade única (padrão: 20)
- `batidas_2densidade`: Número de batidas para 2ª densidade (apenas para materiais de dupla densidade)

### 2. **Migração do Banco de Dados** ✅
- Criada migração `0005_tipomaterial_batidas_tipomaterial_batidas_2densidade.py`
- Migração aplicada com sucesso

### 3. **População de Dados** ✅
Atualizado comando `popular_dados_planilha` com valores de batidas:

| Material          | Batidas (1ª) | Batidas (2ª) | Observação                    |
|-------------------|--------------|--------------|-------------------------------|
| Tafetá            | 20           | 28           | Conforme planilha (J23, J25)  |
| Sarja             | 20           | -            |                               |
| Alta Definição    | 20           | -            |                               |
| Dupla Densidade   | 20           | 28           | Material de dupla densidade   |
| Super Batidas     | 30           | -            | Nome sugere mais batidas      |
| Canvas            | 20           | -            |                               |
| Cetim             | 20           | -            |                               |
| SuperSoft         | 20           | -            |                               |

### 4. **Interface do Usuário** ✅
- Adicionado campo de exibição de batidas no formulário de orçamento
- Campo aparece automaticamente quando o usuário seleciona o tipo de material
- Exibe batidas da 1ª e 2ª densidade (quando aplicável)
- Campo é **somente leitura** (calculado automaticamente)

### 5. **API Endpoint** ✅
- Criado endpoint `/api/material/<id>/batidas/` para buscar batidas do material
- Retorna JSON com batidas e nome do material

## ⚠️ PENDENTE: Impacto nos Cálculos

**IMPORTANTE:** As batidas foram implementadas como **campos informativos**, mas ainda não foram integradas na lógica de cálculo do orçamento.

### Próximos Passos (aguardando definição):

1. **Verificar na planilha Excel:**
   - Como as batidas afetam os valores calculados?
   - Elas alteram algum coeficiente ou fator?
   - Influenciam no preço base, goma, corte?

2. **Implementar lógica de cálculo:**
   - Adicionar batidas na classe `CalculadoraOrcamento`
   - Ajustar fórmulas conforme necessário
   - Atualizar documentação `CALCULO_PLANILHA.md`

## Como Usar:

### No Admin Django:
1. Acesse `/admin/orcamento/tipomaterial/`
2. Edite cada material para definir suas batidas
3. Para materiais de dupla densidade, preencha também `batidas_2densidade`

### No Formulário de Orçamento:
1. Ao selecionar um tipo de material, as batidas aparecem automaticamente
2. Campo é apenas informativo (não editável pelo usuário)
3. Mostra "X batidas" e, se aplicável, "(2ª densidade: Y batidas)"

## Arquivos Modificados:

- ✅ `orcamento/models.py` - Adicionados campos batidas
- ✅ `orcamento/migrations/0005_...py` - Nova migração
- ✅ `orcamento/management/commands/popular_dados_planilha.py` - Dados iniciais
- ✅ `orcamento/templates/orcamento/orcamento_form.html` - Interface
- ✅ `orcamento/views.py` - API endpoint
- ✅ `orcamento/urls.py` - Roteamento

## Para Ajustar os Valores:

Execute novamente o comando de população:
```bash
python manage.py popular_dados_planilha
```

Ou edite manualmente no Django Admin.

