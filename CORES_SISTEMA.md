# 🎨 Sistema de Cores/Variantes

## ✅ Implementado - Baseado na Planilha Excel

O sistema agora suporta **cores/variantes** exatamente como na planilha, incluindo **Dupla Densidade** com 2 conjuntos de cores.

## 📊 Como Funciona

### 1. **Cor do Urdume**
- Campo de seleção com opções:
  - Branco
  - Preto
  - Branco e Preto
  - Vermelho
  - Nenhum

### 2. **Cores por Densidade**

#### Materiais Normais (Tafetá, Sarja, etc.)
- **Apenas 1ª Densidade**
- Tabela com colunas:
  - **Cor**: Posição (Fd=Fundo, 1ª, 2ª, 3ª, 4ª, 5ª, 6ª, 7ª)
  - **Código**: Ex: F01, T30, etc
  - **Unidades**: Quantidade de unidades desta cor
  - **+ Demais**: Quantidade adicional (coluna opcional)
  - **Total**: Soma automática (Unidades + Demais)

#### Dupla Densidade
- **2 Tabelas**: 1ª Densidade E 2ª Densidade
- Cada densidade tem suas próprias cores
- **Total Geral**: Soma as duas densidades

### 3. **Exemplo da Planilha**

**Caso 1: Dupla Densidade**
```
1ª Densidade:
  Fd (F01): 25 + 0 = 25
  1ª (T30): 20 + 0 = 20
  Total: 45

2ª Densidade:
  Fd (?):  25 + ? = 25
  1ª (?):  20 + ? = 20
  Total: 45

TOTAL GERAL: 90
```

**Caso 2: Tafetá (Normal)**
```
1ª Densidade:
  Fd (F01): 25 + 0 = 25
  1ª (T30): 20 + 0 = 20
  Total: 45
```

## 🗄️ Modelo de Dados

### CorOrcamento
```python
class CorOrcamento(models.Model):
    orcamento = ForeignKey(Orcamento)
    
    # Posição da cor
    posicao = CharField(choices=['Fd', '1', '2', '3', '4', '5', '6', '7'])
    
    # Densidade (1ª ou 2ª)
    densidade = CharField(choices=['1', '2'], default='1')
    
    # Código da cor
    codigo_cor = CharField(max_length=20)
    
    # Quantidades
    quantidade_unidades = IntegerField()
    quantidade_demais = IntegerField(default=0)
    
    # Ordem de exibição
    ordem = IntegerField(default=0)
    
    @property
    def total_unidades(self):
        return quantidade_unidades + quantidade_demais
```

### Relacionamento
```python
class Orcamento(models.Model):
    # ... campos existentes ...
    cor_urdume = CharField(choices=[...])
    
    # Relacionamento reverso
    # orcamento.cores.all() - retorna todas as cores
    
    @property
    def is_dupla_densidade(self):
        return 'dupla densidade' in tipo_material.nome.lower()
```

## 💻 Interface (Alpine.js)

### Componente Reativo
```javascript
coresManager() {
    cores1: [],  // 1ª densidade
    cores2: [],  // 2ª densidade
    isDuplaDensidade: false,
    
    // Totalizações automáticas
    totalUnidades1, totalDemais1, totalGeral1
    totalUnidades2, totalDemais2, totalGeral2
    
    // Ações
    adicionarCor1(), removerCor1(index)
    adicionarCor2(), removerCor2(index)
}
```

### Detecção Automática de Dupla Densidade
- Observa o campo `tipo_material`
- Se contém "dupla densidade" no nome:
  - Mostra a 2ª tabela de cores
  - Mostra badge "Dupla Densidade"
  - Calcula totais gerais

## 🎯 Funcionalidades

### ✅ Adicionar Cores Dinamicamente
- Botão "+ Adicionar Cor" em cada densidade
- Linha nova com campos em branco

### ✅ Remover Cores
- Botão de lixeira em cada linha
- Mantém sempre pelo menos 1 cor (Fd=Fundo)

### ✅ Totalizações Automáticas
- **Por Densidade:**
  - Total Unidades
  - Total Demais
  - Total Geral
  
- **Geral (Dupla Densidade):**
  - Soma das 2 densidades

### ✅ Validações
- Posição única por densidade (Fd, 1ª, 2ª, etc)
- Quantidades >= 0
- Código obrigatório

## 📝 Uso no Formulário

### 1. Incluir no Template
```django
{% include 'orcamento/partials/cores_form.html' %}
```

### 2. Processar no Backend
```python
def criar_orcamento(request):
    if request.method == 'POST':
        # ... criar orçamento ...
        
        # Processar cores
        cores_data = json.loads(request.POST.get('cores_data', '{}'))
        
        # 1ª Densidade
        for i, cor in enumerate(cores_data.get('cores1', [])):
            if cor['codigo']:
                CorOrcamento.objects.create(
                    orcamento=orcamento,
                    posicao=cor['posicao'],
                    densidade='1',
                    codigo_cor=cor['codigo'],
                    quantidade_unidades=cor['unidades'],
                    quantidade_demais=cor['demais'],
                    ordem=i
                )
        
        # 2ª Densidade (se houver)
        for i, cor in enumerate(cores_data.get('cores2', [])):
            if cor['codigo']:
                CorOrcamento.objects.create(
                    orcamento=orcamento,
                    posicao=cor['posicao'],
                    densidade='2',
                    codigo_cor=cor['codigo'],
                    quantidade_unidades=cor['unidades'],
                    quantidade_demais=cor['demais'],
                    ordem=i
                )
```

### 3. Exibir no Detalhe
```django
<!-- Cores da 1ª Densidade -->
<h4>1ª Densidade</h4>
<table>
    {% for cor in orcamento.cores.filter(densidade='1') %}
    <tr>
        <td>{{ cor.get_posicao_display }}</td>
        <td>{{ cor.codigo_cor }}</td>
        <td>{{ cor.quantidade_unidades }}</td>
        <td>{{ cor.quantidade_demais }}</td>
        <td>{{ cor.total_unidades }}</td>
    </tr>
    {% endfor %}
</table>

<!-- Cores da 2ª Densidade (se for Dupla Densidade) -->
{% if orcamento.is_dupla_densidade %}
<h4>2ª Densidade</h4>
<table>
    {% for cor in orcamento.cores.filter(densidade='2') %}
    <tr>
        <td>{{ cor.get_posicao_display }}</td>
        <td>{{ cor.codigo_cor }}</td>
        <td>{{ cor.quantidade_unidades }}</td>
        <td>{{ cor.quantidade_demais }}</td>
        <td>{{ cor.total_unidades }}</td>
    </tr>
    {% endfor %}
</table>
{% endif %}
```

## 🎨 Estilização

### Cores das Tabelas
- **1ª Densidade**: Background amarelo claro nos totais
- **2ª Densidade**: Background amarelo claro nos totais
- **Total Geral**: Background verde com borda verde forte

### Badges
- **Dupla Densidade**: Badge amarelo ao lado do título

### Botões
- **Adicionar**: Roxo (`bg-purple-600`)
- **Remover**: Vermelho (`text-red-600`)

## 📊 Totalizações na Planilha vs Sistema

| Planilha | Sistema |
|----------|---------|
| Soma manual | Soma automática (Alpine.js) |
| Total por densidade | ✅ Implementado |
| Total geral (dupla) | ✅ Implementado |
| Coluna "Demais" | ✅ Implementado |

## 🔄 Fluxo Completo

### 1. Criar Orçamento
```
1. Selecionar Material
   ↓
2. Sistema detecta se é Dupla Densidade
   ↓
3. Mostra tabela(s) de cores apropriadas
   ↓
4. Usuário adiciona cores
   ↓
5. Totais calculados automaticamente
   ↓
6. Salvar: Cores são gravadas no banco
```

### 2. Editar Orçamento
```
1. Carregar orçamento existente
   ↓
2. Carregar cores do banco
   ↓
3. Popular tabelas com cores existentes
   ↓
4. Permitir edição
   ↓
5. Salvar alterações
```

### 3. Visualizar Orçamento
```
1. Exibir tabela de cores
   ↓
2. Mostrar totais por densidade
   ↓
3. Se dupla: mostrar total geral
```

## 🎯 Próximos Passos Sugeridos

- [ ] Adicionar cores pré-definidas (catálogo)
- [ ] Permitir copiar cores de outro orçamento
- [ ] Histórico de cores mais usadas
- [ ] Validar total de cores vs quantidade de unidades
- [ ] Exportar tabela de cores em PDF

## ✅ Status

✅ **Modelo criado**  
✅ **Migração aplicada**  
✅ **Interface Alpine.js**  
✅ **Admin configurado**  
⏳ **Integração com formulário** (próximo passo)

---

**Versão**: 2.2.0  
**Data**: Novembro 2024  
**Feature**: Sistema de Cores/Variantes

