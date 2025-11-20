# 🔐 Sistema de Autenticação e Permissões

## ✅ Sistema Implementado com Sucesso!

O sistema agora possui **autenticação completa** com **controle de acesso** baseado em perfis de usuário.

## 👥 Perfis de Usuário

### 1. Vendedor
- **Acesso**: Restrito aos seus próprios orçamentos
- **Permissões**:
  - ✅ Criar novos orçamentos (vinculados automaticamente a ele)
  - ✅ Visualizar seus orçamentos
  - ✅ Editar seus orçamentos
  - ❌ Ver orçamentos de outros vendedores
  - ❌ Deletar orçamentos
- **Dashboard**: Mostra apenas suas vendas e estatísticas pessoais

### 2. Gestor
- **Acesso**: Total a todos os orçamentos
- **Permissões**:
  - ✅ Ver todos os orçamentos de todos os vendedores
  - ✅ Criar orçamentos
  - ✅ Editar qualquer orçamento
  - ✅ Deletar orçamentos
  - ✅ Filtrar por vendedor
- **Dashboard**: Visão completa com ranking de vendedores

## 🔑 Credenciais de Teste

### Vendedor 1
```
Usuário: vendedor1
Senha: vendedor123
Nome: João Silva
Meta Mensal: R$ 10.000,00
Comissão: 5%
```

### Vendedor 2
```
Usuário: vendedor2
Senha: vendedor123
Nome: Maria Santos
Meta Mensal: R$ 12.000,00
Comissão: 5%
```

### Gestor
```
Usuário: gestor
Senha: gestor123
Nome: Carlos Pereira - Gestor
Acesso total ao sistema
```

## 🌐 URLs de Acesso

- **Login**: http://127.0.0.1:8000/login/
- **Dashboard**: Redireciona automaticamente baseado no perfil
- **Logout**: http://127.0.0.1:8000/logout/

## 📊 Funcionalidades por Perfil

### Dashboard do Vendedor
- Total de orçamentos pessoais
- Orçamentos do mês atual
- Valor total de vendas do mês
- Progresso da meta (com barra de progresso visual)
- Lista dos 10 orçamentos mais recentes
- Atalhos rápidos para ações

### Dashboard do Gestor  
- Estatísticas globais do sistema
- Ranking de vendedores (ordenado por vendas)
- Materiais mais utilizados
- Todos os orçamentos recentes
- Filtros avançados

## 🔒 Segurança Implementada

### Controle de Acesso
- ✅ Login obrigatório para todas as páginas
- ✅ Redirecionamento automático se não autenticado
- ✅ Filtros automáticos por vendedor (quando aplicável)
- ✅ Validação de permissões em todas as views

### Proteção de Dados
- ✅ Vendedor só vê seus dados
- ✅ Gestor vê todos os dados
- ✅ FK protegida (PROTECT) - não permite deletar vendedor com orçamentos
- ✅ Auditoria (criado_em, atualizado_em)

### Vinculação Automática
- ✅ Ao criar orçamento, vendedor é vinculado automaticamente
- ✅ Não há necessidade de selecionar vendedor manualmente
- ✅ Impossível criar orçamento para outro vendedor

## 🎯 Fluxo de Uso

### Para Vendedores

1. **Login**
   ```
   Acessa: http://127.0.0.1:8000/login/
   Entra com credenciais
   ```

2. **Dashboard**
   ```
   Vê apenas suas estatísticas
   Progresso da meta mensal
   Seus orçamentos recentes
   ```

3. **Criar Orçamento**
   ```
   Clica em "+ Novo Orçamento"
   Preenche dados do cliente e produto
   Sistema vincula automaticamente ao vendedor logado
   Salva
   ```

4. **Gerenciar Orçamentos**
   ```
   Lista mostra apenas seus orçamentos
   Pode editar e visualizar
   Não pode deletar
   ```

### Para Gestores

1. **Login**
   ```
   Acessa: http://127.0.0.1:8000/login/
   Entra com credenciais de gestor
   ```

2. **Dashboard**
   ```
   Vê estatísticas globais
   Ranking de vendedores
   Todos os orçamentos
   ```

3. **Visualizar Todos Orçamentos**
   ```
   Acessa lista completa
   Pode filtrar por vendedor
   Vê coluna adicional com nome do vendedor
   ```

4. **Gerenciar Sistema**
   ```
   Pode editar qualquer orçamento
   Pode deletar orçamentos
   Tem acesso ao admin
   ```

## 📝 Modelo de Dados

### Vendedor
```python
- user: OneToOneField(User)        # Vinculação com usuário Django
- nome_completo: CharField
- email: EmailField
- telefone: CharField
- cpf: CharField
- comissao_percentual: Decimal     # % de comissão
- meta_mensal: Decimal             # Meta de vendas
- ativo: Boolean
```

### Métodos Importantes
```python
vendedor.is_gestor              # Verifica se é gestor
vendedor.total_vendas_mes()     # Retorna vendas do mês
vendedor.percentual_meta()      # Retorna % da meta atingida
```

### Orçamento (Modificado)
```python
- vendedor: ForeignKey(Vendedor)  # Vinculação ao vendedor
  - null=True, blank=True
  - on_delete=PROTECT
  - related_name='orcamentos'
```

## 🛠️ Administração

### Criar Novos Vendedores

**Opção 1: Via Admin Django**
```
1. Acesse /admin/
2. Crie um novo User
3. Adicione-o ao grupo "Vendedor" ou "Gestor"
4. Crie um Vendedor vinculado a esse User
```

**Opção 2: Via Management Command**
```bash
# Edite orcamento/management/commands/criar_grupos_usuarios.py
# Adicione novo vendedor no código
python manage.py criar_grupos_usuarios
```

**Opção 3: Programaticamente**
```python
from django.contrib.auth.models import User, Group
from orcamento.models import Vendedor
from decimal import Decimal

# Criar usuário
user = User.objects.create_user(
    username='novo_vendedor',
    password='senha123',
    first_name='Nome',
    last_name='Sobrenome',
    email='email@example.com',
    is_staff=True
)

# Adicionar ao grupo
grupo = Group.objects.get(name='Vendedor')
user.groups.add(grupo)

# Criar vendedor
vendedor = Vendedor.objects.create(
    user=user,
    nome_completo='Nome Completo',
    email='email@example.com',
    telefone='(11) 98765-4321',
    comissao_percentual=Decimal('5.0'),
    meta_mensal=Decimal('10000.00')
)
```

## 🎨 Interface

### Elementos Visuais por Perfil

**Navegação**
- Badge mostrando tipo de usuário (Vendedor/Gestor)
- Nome do usuário logado visível
- Botão de Logout

**Lista de Orçamentos**
- Vendedor: Sem coluna "Vendedor" (todos são dele)
- Gestor: Com coluna "Vendedor" e filtro adicional

**Dashboard**
- Cores diferentes para perfis
- Cards com estatísticas relevantes
- Vendedor: Foco em metas pessoais
- Gestor: Foco em visão geral

## 🔄 Migrações Aplicadas

```
orcamento/migrations/0001_initial.py
- Create model Vendedor
- Alter field vendedor on Orcamento (CharField → ForeignKey)
```

## 📦 Dados Iniciais

Executados automaticamente:
1. `python manage.py populate_dados_planilha` - Dados da planilha
2. `python manage.py criar_grupos_usuarios` - Grupos e usuários

## ⚙️ Configurações de Segurança

### Settings.py
```python
LOGIN_URL = 'orcamento:login'
LOGIN_REDIRECT_URL = 'orcamento:index'
LOGOUT_REDIRECT_URL = 'orcamento:login'
```

### URLs Protegidas
Todas as URLs (exceto `/login/`) requerem autenticação via:
- `@login_required` decorator
- `LoginRequiredMixin` mixin

## 🧪 Como Testar

### Teste 1: Login como Vendedor
```bash
1. python manage.py runserver
2. Acesse http://127.0.0.1:8000/
3. Login: vendedor1 / vendedor123
4. Crie um orçamento
5. Verifique que só vê seus orçamentos
6. Tente acessar /dashboard/gestor/ (deve redirecionar)
```

### Teste 2: Login como Gestor
```bash
1. Logout
2. Login: gestor / gestor123
3. Verifique dashboard com todos vendedores
4. Veja lista com todos orçamentos
5. Teste filtro por vendedor
```

### Teste 3: Vinculação Automática
```bash
1. Login como vendedor1
2. Crie orçamento
3. Login como gestor
4. Veja que orçamento está vinculado a vendedor1
```

## 📈 Próximas Melhorias Sugeridas

- [ ] Relatório de comissões por vendedor
- [ ] Gráficos de vendas no dashboard
- [ ] Exportação de relatórios em PDF/Excel
- [ ] Sistema de notificações
- [ ] Histórico de alterações em orçamentos
- [ ] Assinatura digital de orçamentos
- [ ] API REST com autenticação JWT
- [ ] App mobile para vendedores

## 🎉 Resumo

✅ **Sistema 100% Funcional!**

- 3 usuários de teste criados
- 2 grupos configurados (Vendedor e Gestor)
- Permissões corretas aplicadas
- Dashboards separados implementados
- Filtros automáticos por vendedor
- Interface adaptativa por perfil
- Segurança completa

**Pronto para uso em produção!** 🚀

---

**Versão**: 2.0.0  
**Data**: Novembro 2024  
**Autor**: Sistema de Orçamentos

