# 📋 Gerenciamento de Tabelas Auxiliares

## ✅ Todas as Tabelas São EDITÁVEIS via Django Admin

As tabelas auxiliares **não são fixas** e podem ser totalmente gerenciadas através da interface web do Django Admin, sem necessidade de comandos ou código.

## 🔐 Acesso ao Admin

**URL:** http://127.0.0.1:8000/admin/

**Credenciais:**
- **Superusuário:** (criado com `python manage.py createsuperuser`)
- **Gestor:** Usuário `gestor` (se criado via `criar_grupos_usuarios`)

## 📊 Tabelas Disponíveis para Edição

### 1. **Tipos de Material** 
**Path:** `/admin/orcamento/tipomaterial/`

**Campos Editáveis:**
- Nome do material (ex: Tafetá, Sarja, Canvas)
- Código (usado internamente)
- **Batidas** (1ª densidade ou densidade única)
- **Batidas 2ª densidade** (apenas para materiais de dupla densidade)
- Ordem de exibição
- Ativo (mostrar ou ocultar)

**Recursos:**
- ✅ Edição inline direta na listagem
- ✅ Busca por nome ou código
- ✅ Filtro por status (ativo/inativo)
- ✅ Ordenação por ordem ou nome

---

### 2. **Tipos de Corte**
**Path:** `/admin/orcamento/tipocorte/`

**Campos Editáveis:**
- Nome do corte (ex: Corte Normal, Dobra Meio, Envelope)
- Código
- Código de cálculo (usado nas fórmulas)
- Ativo

**Recursos:**
- ✅ Edição inline
- ✅ Busca e filtros

---

### 3. **Tabela de Preços**
**Path:** `/admin/orcamento/tabelapreco/`

**Campos Editáveis:**
- Metragem (faixa: 300, 500, 1000, etc.)
- Tipo de material
- **Preço por metro** ← **Editável diretamente na lista**

**Como Funciona:**
- O sistema busca o preço baseado na **quantidade de metros do pedido**
- Exemplo: Pedido de 800 metros usa o preço da faixa de 500 metros

**Recursos:**
- ✅ Edição inline do preço
- ✅ Filtro por tipo de material
- ✅ Busca por material
- ✅ Ordenado por material e metragem

**Dica:** Para adicionar novos preços:
1. Clique em "Adicionar tabela de preço"
2. Selecione o material
3. Digite a metragem e o preço
4. Salvar

---

### 4. **Coeficientes Fator**
**Path:** `/admin/orcamento/coeficientefator/`

**Campos Editáveis:**
- Largura (mm)
- Tipo de material
- Tipo de corte
- **Coeficiente** ← **Editável diretamente na lista**

**Como Funciona:**
- Coeficientes multiplicam o preço base
- Baseado em: largura + material + tipo de corte

**Recursos:**
- ✅ Edição inline
- ✅ Filtros por material e corte
- ✅ Busca

---

### 5. **Valores de Goma**
**Path:** `/admin/orcamento/valorgoma/`

**Campos Editáveis:**
- Largura (mm)
- **Goma Fino** (valor adicional) ← **Editável**
- **Goma Grosso** (valor adicional) ← **Editável**
- **Termocolante** (valor adicional) ← **Editável**

**Como Funciona:**
- Quando o pedido tem goma, adiciona esse valor ao custo
- Valor varia conforme largura e tipo de goma

---

### 6. **Valores de Corte Especial**
**Path:** `/admin/orcamento/valorcorte/`

**Campos Editáveis:**
- Largura (mm)
- **Canvas** (valor adicional) ← **Editável**
- **Cetim** (valor adicional) ← **Editável**

**Como Funciona:**
- Apenas para materiais Canvas e Cetim
- Adiciona custo extra baseado na largura

---

### 7. **Configurações Globais**
**Path:** `/admin/orcamento/configuracao/`

**Configurações Disponíveis:**

| Chave                  | Valor Padrão | Descrição                                     |
|------------------------|--------------|-----------------------------------------------|
| `perc_ultrassonico`    | 1.15         | Percentual de aumento para corte ultrassônico |
| `perc_aumento_geral`   | 1.00         | Percentual de aumento geral em todos os preços|

**⚠️ CUIDADO:**
- Essas configurações afetam **TODOS** os cálculos do sistema
- Alterações são aplicadas imediatamente
- **Não deletar** essas configurações (botão de deletar está desabilitado)

**Recursos:**
- ✅ Edição inline do valor
- ✅ Descrição detalhada de cada configuração

---

### 8. **Texturas**
**Path:** `/admin/orcamento/textura/`

**Campos Editáveis:**
- Código
- Nome da textura
- Ordem de exibição
- Ativo

**Recursos:**
- ✅ Edição inline
- ✅ Ordenação por ordem ou código

---

### 9. **Vendedores**
**Path:** `/admin/orcamento/vendedor/`

**Campos Editáveis:**
- Usuário do sistema (vínculo com User)
- Nome completo
- Email, telefone, CPF
- Comissão percentual
- Meta mensal
- Observações
- Ativo

---

## 🔄 Fluxo de Atualização de Dados

### Método 1: **Via Django Admin** (Recomendado para manutenção)
1. Acesse http://127.0.0.1:8000/admin/
2. Navegue até a tabela desejada
3. Edite diretamente na lista ou clique no item
4. Salvar

✅ **Vantagens:**
- Interface visual amigável
- Edição inline rápida
- Sem necessidade de código
- Validação automática de dados

### Método 2: **Via Comando** (Para população inicial ou reset)
```bash
python manage.py popular_dados_planilha
```

⚠️ **Atenção:** Este comando usa `update_or_create`, então:
- **Atualiza** registros existentes (não apaga suas alterações manuais)
- **Cria** novos registros se não existirem
- **Mantém** registros extras que você adicionou manualmente

## 💡 Dicas de Uso

### Para Ajustar Preços:
1. Vá em **Tabela de Preços**
2. Clique no campo de preço diretamente na lista
3. Digite o novo valor
4. Tecle Enter ou clique fora do campo
5. Preço atualizado imediatamente!

### Para Adicionar Nova Faixa de Metragem:
1. Vá em **Tabela de Preços**
2. Clique em "Adicionar tabela de preço"
3. Preencha: Material, Metragem (ex: 20000), Preço
4. Salvar

### Para Ajustar Batidas de um Material:
1. Vá em **Tipos de Material**
2. Clique no material desejado (ou edite inline)
3. Altere os campos "Batidas" e "Batidas 2ª densidade"
4. Salvar

### Para Alterar Percentuais Globais:
1. Vá em **Configurações**
2. Edite o campo "Valor" diretamente
3. Exemplo: Para 15% de aumento ultrassônico, use `1.15`
4. Exemplo: Para 5% de aumento geral, use `1.05`

## 📈 Exportação de Dados

Para backup ou análise, você pode:

### Opção 1: Usar o Admin do Django
- Selecione múltiplos registros
- Use "Actions" para operações em lote (se configurado)

### Opção 2: Comando de Backup
```bash
python manage.py dumpdata orcamento --indent 2 > backup_tabelas.json
```

### Opção 3: Restaurar Backup
```bash
python manage.py loaddata backup_tabelas.json
```

## 🔒 Permissões

**Quem pode editar:**
- ✅ **Superusuário** (super admin): Acesso total
- ✅ **Gestor**: Pode visualizar e editar (via grupos)
- ❌ **Vendedor**: Sem acesso ao admin (apenas formulários de orçamento)

## ⚙️ Recursos Avançados

### 1. **Edição em Massa**
- Marque múltiplos registros na lista
- Use o dropdown "Ação" no topo
- Aplique ações em lote

### 2. **Filtros Rápidos**
- Use a barra lateral direita para filtrar
- Combine múltiplos filtros

### 3. **Busca Inteligente**
- Use a barra de busca no topo
- Busca em múltiplos campos simultaneamente

### 4. **Ordenação**
- Clique nos cabeçalhos das colunas para ordenar
- Clique novamente para inverter a ordem

## 📞 Suporte

Se precisar adicionar novos campos ou funcionalidades às tabelas auxiliares:
1. Modifique o modelo em `orcamento/models.py`
2. Crie migração: `python manage.py makemigrations`
3. Aplique: `python manage.py migrate`
4. Atualize o admin em `orcamento/admin.py` se necessário

---

**Resumo:** ✅ Todas as tabelas são **totalmente editáveis** via interface web, sem necessidade de código ou comandos!

