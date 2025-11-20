# 📋 Sistema de Orçamentos de Etiquetas

Sistema inteligente para cálculo de orçamentos de etiquetas personalizadas desenvolvido em Django, com Alpine.js, Tailwind CSS e HTMX.

## 🚀 Tecnologias Utilizadas

- **Django 4.2** - Framework web Python
- **Alpine.js** - Framework JavaScript reativo e leve
- **Tailwind CSS** - Framework CSS utilitário
- **HTMX** - Biblioteca para interações AJAX modernas
- **SQLite** - Banco de dados (desenvolvimento)

## 📋 Funcionalidades

### 🆕 Novo! Sistema de Autenticação Completo

- **🔐 Login e Senha**: Cada vendedor tem acesso individual ao sistema
- **👥 Perfis de Usuário**: Vendedores e Gestores com permissões diferentes
- **🎯 Vinculação Automática**: Orçamentos vinculados automaticamente ao vendedor logado
- **📊 Dashboards Separados**: Interface personalizada para cada tipo de usuário
- **🔒 Controle de Acesso**: Vendedor vê apenas seus orçamentos, gestor vê tudo
- **📈 Metas e Comissões**: Acompanhamento de metas mensais e percentuais de comissão

### ✨ Principais Recursos

- **Cálculo Inteligente**: Sistema automático de cálculo baseado em tabelas dinâmicas e coeficientes
- **Cálculo em Tempo Real**: Interface responsiva com HTMX para cálculos instantâneos
- **Múltiplos Tipos de Material**: Tafetá, Sarja, Alta Definição, Dupla Densidade, Canvas, Cetim, etc.
- **Tipos de Corte Diversos**: Corte Normal, Meio Corte, Dobra Meio, Dobra Cantos, Envelope, etc.
- **Dashboard Completo**: Visualização de estatísticas e relatórios
- **Gestão de Clientes**: Cadastro completo com tipos de cliente e histórico
- **Opções Avançadas**: Gomas (fino, grosso, termocolante), corte ultrassônico
- **Texturas Personalizadas**: Mais de 30 texturas disponíveis

### 🎯 Sistema de Cálculo

O sistema implementa a lógica complexa da planilha Excel original com:

- Tabelas de preços por metragem e tipo de material
- Coeficientes de fator (CF) baseados em largura e tipo
- Coeficientes de corte (CC) calculados dinamicamente
- Valores de goma por largura e tipo
- Percentuais de ajuste (ultrassônico, tipo de cliente)
- Cálculo de valores por metro, milheiro, unidade e total

## 🔧 Instalação

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Passos de Instalação

1. **Clone o repositório** (ou extraia os arquivos)

```bash
cd D:\projetos\futura_cursor
```

2. **Crie um ambiente virtual**

```bash
python -m venv venv
```

3. **Ative o ambiente virtual**

```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. **Instale as dependências**

```bash
pip install -r requirements.txt
```

5. **Execute as migrações do banco de dados**

```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Popule o banco de dados com dados iniciais**

```bash
python manage.py popular_dados_planilha
```

7. **Crie grupos e usuários de teste**

```bash
python manage.py criar_grupos_usuarios
```

Isso criará 3 usuários prontos para uso:
- **vendedor1** (senha: vendedor123) - Vendedor João Silva
- **vendedor2** (senha: vendedor123) - Vendedora Maria Santos  
- **gestor** (senha: gestor123) - Gestor Carlos Pereira

8. **(Opcional) Crie um superusuário para acessar o admin**

```bash
python manage.py createsuperuser
```

9. **Execute o servidor de desenvolvimento**

```bash
python manage.py runserver
```

10. **Acesse o sistema**

- **Login**: http://127.0.0.1:8000/login/
- Interface principal: http://127.0.0.1:8000/
- Painel administrativo: http://127.0.0.1:8000/admin/

## 📖 Guia de Uso

### 🔐 Primeiro Acesso

1. Acesse http://127.0.0.1:8000/
2. Faça login com uma das credenciais de teste:
   - **Vendedor**: `vendedor1` / `vendedor123`
   - **Gestor**: `gestor` / `gestor123`
3. Será redirecionado para o dashboard apropriado

### 👤 Como Vendedor

**Dashboard Pessoal**
- Veja suas estatísticas individuais
- Acompanhe progresso da meta mensal
- Visualize seus últimos orçamentos

**Criar Orçamento**
1. Clique em "+ Novo Orçamento"
2. Preencha os dados do cliente
3. Defina as especificações (material, dimensões, corte)
4. Informe quantidades (metros e unidades)
5. Valores calculados em tempo real
6. Salve - orçamento será vinculado automaticamente a você!

**Seus Orçamentos**
- Veja apenas os orçamentos que você criou
- Edite e visualize detalhes
- Não pode ver orçamentos de outros vendedores

### 👨‍💼 Como Gestor

**Dashboard Completo**
- Veja estatísticas de todos os vendedores
- Ranking de performance
- Materiais mais utilizados
- Todos os orçamentos do sistema

**Gerenciar Orçamentos**
- Visualize TODOS os orçamentos
- Filtre por vendedor específico
- Edite qualquer orçamento
- Acesse relatórios completos

### Editando Configurações

Acesse o painel administrativo para:

- Adicionar/editar tipos de material
- Configurar tabelas de preços
- Ajustar coeficientes de cálculo
- Modificar valores de goma
- Gerenciar texturas disponíveis

## 🎨 Estrutura do Projeto

```
futura_cursor/
├── config/                 # Configurações do Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── orcamento/             # App principal
│   ├── models.py          # Modelos de dados
│   ├── views.py           # Views
│   ├── forms.py           # Formulários
│   ├── calculadora.py     # Lógica de cálculo
│   ├── admin.py           # Configuração do admin
│   ├── urls.py            # URLs do app
│   ├── templates/         # Templates HTML
│   │   ├── base.html
│   │   └── orcamento/
│   │       ├── index.html
│   │       ├── dashboard.html
│   │       ├── orcamento_list.html
│   │       ├── orcamento_form.html
│   │       ├── orcamento_detail.html
│   │       └── partials/
│   └── management/
│       └── commands/
│           └── popular_dados_planilha.py
├── static/                # Arquivos estáticos
├── PlanilhaExcel/         # Planilha original (referência)
├── manage.py
└── requirements.txt
```

## 🔍 Modelos de Dados

### Principais Entidades

- **Vendedor**: 🆕 Vendedores do sistema com metas e comissões
- **TipoMaterial**: Tipos de material (Tafetá, Sarja, etc.)
- **TipoCorte**: Tipos de corte disponíveis
- **TabelaPreco**: Preços por metragem e material
- **CoeficienteFator**: Coeficientes de cálculo
- **ValorGoma**: Valores de goma por largura
- **Orcamento**: Orçamentos completos (vinculados a vendedores)
- **Configuracao**: Configurações globais do sistema
- **Textura**: Texturas disponíveis

## 🧮 Lógica de Cálculo

O sistema implementa a seguinte fórmula de cálculo:

```
1. Obter preço base (VLOOKUP na tabela de preços)
2. Aplicar coeficiente fator (baseado em largura e tipo)
3. Adicionar valor de goma (se aplicável)
4. Adicionar valor de corte especial (canvas/cetim)
5. Aplicar coeficiente de corte (CC)
6. Aplicar percentual ultrassônico (se aplicável)
7. Aplicar percentual de aumento geral
8. Aplicar fator de tipo de cliente
9. Calcular valores finais (metro, milheiro, unidade, total)
```

## 🎯 Recursos do Frontend

### Alpine.js
- Reatividade de dados no formulário
- Atualização dinâmica de valores
- Controle de estado de componentes

### HTMX
- Cálculos em tempo real sem recarregar página
- Atualizações parciais de conteúdo
- Indicadores de carregamento

### Tailwind CSS
- Interface moderna e responsiva
- Componentes estilizados
- Design system consistente

## 🔐 Segurança e Autenticação

### Sistema de Login
- ✅ Autenticação obrigatória em todas as páginas
- ✅ Login individual por vendedor
- ✅ Senhas criptografadas (hash)
- ✅ Sessões seguras

### Controle de Acesso
- ✅ Vendedores veem apenas seus dados
- ✅ Gestores têm acesso completo
- ✅ Grupos e permissões do Django
- ✅ Proteção contra exclusão acidental (PROTECT)

### Proteção Geral
- ✅ CSRF protection habilitado
- ✅ Validação de dados no backend
- ✅ Sanitização de inputs
- ✅ Permissões de acesso ao admin

### 📚 Documentação de Autenticação
- **[AUTENTICACAO.md](AUTENTICACAO.md)** - Documentação técnica completa
- **[COMO_USAR_AUTENTICACAO.md](COMO_USAR_AUTENTICACAO.md)** - Guia prático passo a passo
- **[TESTE_AUTENTICACAO.md](TESTE_AUTENTICACAO.md)** - Checklist de testes

## ✅ Funcionalidades Implementadas

- [x] ✅ Sistema de autenticação completo
- [x] ✅ Perfis de usuário (Vendedor/Gestor)
- [x] ✅ Vinculação automática de orçamentos
- [x] ✅ Dashboards personalizados
- [x] ✅ Controle de acesso por permissões
- [x] ✅ Metas e comissões por vendedor
- [x] ✅ Ranking de vendedores
- [x] ✅ Cálculo em tempo real (HTMX)
- [x] ✅ Interface moderna (Tailwind CSS)
- [x] ✅ Reatividade (Alpine.js)

## 🚀 Próximas Melhorias Sugeridas

- [ ] Exportação de orçamentos em PDF
- [ ] Envio de orçamentos por e-mail
- [ ] Gráficos de vendas e estatísticas
- [ ] Relatório de comissões
- [ ] Sistema de aprovação de orçamentos
- [ ] Histórico de alterações
- [ ] API REST para integração
- [ ] Importação de dados de planilhas Excel
- [ ] Sistema de notificações
- [ ] App mobile para vendedores

## 📝 Licença

Este projeto foi desenvolvido como solução personalizada.

## 👨‍💻 Desenvolvimento

Desenvolvido com Django, Alpine.js, Tailwind CSS e HTMX.

## 📞 Suporte

Para dúvidas ou sugestões, consulte a documentação ou entre em contato com o desenvolvedor.

---

**Versão**: 2.0.0 🎉  
**Data**: Novembro 2024  
**Novidade**: Sistema de Autenticação Completo!

