# 🚀 Como Usar o Sistema com Autenticação

## Guia Rápido para Início

### 1. Iniciar o Servidor

```bash
python manage.py runserver
```

### 2. Acessar o Sistema

Abra seu navegador em: **http://127.0.0.1:8000/**

O sistema irá redirecionar automaticamente para a página de login.

## 📋 Cenários de Uso

### Cenário 1: Sou um Vendedor

#### Primeiro Acesso
1. Acesse: http://127.0.0.1:8000/login/
2. Use as credenciais:
   - **Usuário**: `vendedor1`
   - **Senha**: `vendedor123`
3. Clique em **Entrar**

#### Após o Login
- Você será direcion para seu **Dashboard Pessoal**
- Verá suas estatísticas:
  - Total de orçamentos
  - Orçamentos do mês
  - Valor total de vendas
  - Progresso da meta (com barra visual)

#### Criar Novo Orçamento
1. Clique em **"+ Novo Orçamento"** (botão verde)
2. Preencha os dados:
   - **Dados do Cliente** (nome, tipo, contato)
   - **Especificações do Produto** (material, dimensões, corte)
   - **Quantidades** (metros, unidades)
   - **Opções** (goma, ultrassônico)
3. Observe os valores sendo calculados **em tempo real**
4. Clique em **"💾 Salvar Orçamento"**
5. O orçamento será automaticamente vinculado a você!

#### Ver Seus Orçamentos
1. Clique em **"Orçamentos"** no menu
2. Você verá **APENAS seus orçamentos**
3. Use os filtros para buscar:
   - Por nome de cliente
   - Por tipo de material
4. Clique em **"Ver"** para detalhes
5. Clique em **"Editar"** para modificar

#### Acompanhar Meta
- No dashboard, veja a barra de progresso da meta
- Verde = atingindo bem
- Amarelo/Laranja = atenção
- Vermelho = abaixo do esperado

---

### Cenário 2: Sou um Gestor

#### Primeiro Acesso
1. Acesse: http://127.0.0.1:8000/login/
2. Use as credenciais:
   - **Usuário**: `gestor`
   - **Senha**: `gestor123`
3. Clique em **Entrar**

#### Após o Login
- Você será direcionado para o **Dashboard do Gestor**
- Verá estatísticas globais:
  - Total de orçamentos (todos)
  - Orçamentos do mês
  - Valor total em vendas
  - **Ranking de vendedores** (por performance)

#### Ver Todos os Orçamentos
1. Clique em **"Orçamentos"** no menu
2. Você verá **TODOS os orçamentos de TODOS os vendedores**
3. Note a coluna extra: **"Vendedor"**
4. Use filtros avançados:
   - Por cliente
   - Por material
   - **Por vendedor** (filtro exclusivo para gestor)

#### Análise de Vendedores
- No dashboard, veja o **Ranking de Vendedores**
- Cada vendedor mostra:
  - Nome
  - Quantidade de orçamentos
  - Valor total vendido
  - % da meta atingida

#### Gerenciar Orçamentos
- Pode editar qualquer orçamento
- Pode visualizar detalhes completos
- Pode deletar se necessário (via admin)

---

## 🎯 Funcionalidades Especiais

### Para Vendedores

#### Meta Mensal
Sua meta é definida pelo gestor. Acompanhe seu progresso:
```
Vendedor 1 (João): Meta de R$ 10.000,00
Vendedor 2 (Maria): Meta de R$ 12.000,00
```

#### Comissões
Você recebe uma comissão percentual sobre suas vendas:
```
Padrão: 5% sobre o valor total dos orçamentos
```

#### Restrições
- ❌ Não pode ver orçamentos de outros vendedores
- ❌ Não pode editar orçamentos de outros
- ❌ Não pode deletar orçamentos
- ❌ Não tem acesso ao painel de gestor

### Para Gestores

#### Visão Completa
- ✅ Vê TODOS os orçamentos
- ✅ Filtra por qualquer vendedor
- ✅ Acessa estatísticas globais
- ✅ Vê ranking de performance

#### Administração
- ✅ Pode editar qualquer orçamento
- ✅ Pode excluir se necessário
- ✅ Acesso ao admin Django (/admin/)
- ✅ Pode criar novos vendedores

---

## 💡 Dicas Práticas

### Para Vendedores

**1. Crie Orçamentos Rapidamente**
- Use a funcionalidade de cálculo em tempo real
- Não precisa fazer contas! O sistema calcula tudo

**2. Acompanhe sua Meta**
- Entre no dashboard diariamente
- Veja quanto falta para atingir a meta
- Planeje seus próximos orçamentos

**3. Organize Seus Orçamentos**
- Use o campo "Número do Pedido"
- Preencha observações importantes
- Mantenha dados de clientes atualizados

### Para Gestores

**1. Monitore a Equipe**
- Verifique o ranking diariamente
- Identifique vendedores com baixa performance
- Reconheça os melhores performers

**2. Analise Tendências**
- Veja quais materiais vendem mais
- Identifique padrões de vendas
- Ajuste estratégias conforme necessário

**3. Gerencie Metas**
- Ajuste metas via admin Django
- Acompanhe % de atingimento
- Defina comissões adequadas

---

## 🔄 Fluxo Completo de Venda

### Passo a Passo (Vendedor)

```
1. LOGIN
   ↓
2. DASHBOARD
   → Ver progresso da meta
   → Ver orçamentos recentes
   ↓
3. NOVO ORÇAMENTO
   → Preencher dados do cliente
   → Definir produto (material, dimensões)
   → Ver cálculo em tempo real
   → Salvar
   ↓
4. ACOMPANHAMENTO
   → Ver orçamento na lista
   → Editar se necessário
   → Mostrar ao cliente
   ↓
5. META
   → Verificar progresso
   → Comemorar quando atingir!
```

### Passo a Passo (Gestor)

```
1. LOGIN
   ↓
2. DASHBOARD GESTOR
   → Ver estatísticas globais
   → Analisar ranking
   ↓
3. ANÁLISE
   → Filtrar por vendedor
   → Ver orçamentos específicos
   → Identificar oportunidades
   ↓
4. GESTÃO
   → Ajustar metas
   → Orientar equipe
   → Tomar decisões
```

---

## 🆘 Problemas Comuns

### "Não consigo fazer login"
✅ Verifique se está usando as credenciais corretas
✅ Usuário: vendedor1, vendedor2 ou gestor
✅ Senha: vendedor123 ou gestor123
✅ Respeite maiúsculas e minúsculas

### "Não vejo orçamentos de outros vendedores"
✅ Isso é normal! Vendedores só veem seus próprios orçamentos
✅ Apenas gestores veem todos

### "Quero criar um orçamento para outro vendedor"
❌ Não é possível! Cada vendedor cria apenas para si
❌ Se for gestor, o orçamento será vinculado a você também

### "Esqueci minha senha"
✅ Apenas o administrador pode redefinir
✅ Acesse /admin/ como superuser
✅ Ou peça ao gestor do sistema

---

## 🎓 Casos de Uso Reais

### Caso 1: Vendedor Iniciante

**João acabou de entrar na empresa:**

1. Recebeu login: `vendedor1` / `vendedor123`
2. Fez primeiro acesso
3. Viu que sua meta é R$ 10.000,00
4. Criou 5 orçamentos no primeiro dia
5. Acompanha progresso diariamente
6. Atingiu 45% da meta na primeira semana!

### Caso 2: Vendedora Experiente

**Maria é top performer:**

1. Login: `vendedor2` / `vendedor123`
2. Meta mais alta: R$ 12.000,00
3. Cria 15-20 orçamentos por semana
4. Sempre atinge 100%+ da meta
5. Ganha destaque no ranking do gestor
6. Tem comissões maiores

### Caso 3: Gestor Monitorando

**Carlos gerencia a equipe:**

1. Login: `gestor` / `gestor123`
2. Vê que João está em 45% (ok)
3. Vê que Maria está em 120% (excelente!)
4. Identifica que Tafetá é o material mais vendido
5. Ajusta metas para o próximo mês
6. Parabeniza Maria publicamente

---

## 📞 Suporte

Se precisar de ajuda:
1. Consulte esta documentação
2. Verifique o README.md principal
3. Entre em contato com o administrador do sistema

---

**Sistema 100% Pronto!** 🎉

Boas vendas! 💰

---

**Versão**: 2.0.0  
**Última Atualização**: Novembro 2024

