# 🚀 Guia de Início Rápido

## Sistema Já Configurado!

O sistema de orçamentos já está pronto para uso. Siga os passos abaixo para começar:

## ✅ Status da Instalação

- ✅ Projeto Django criado
- ✅ Modelos de dados configurados
- ✅ Banco de dados criado e populado
- ✅ Templates com Tailwind CSS, Alpine.js e HTMX
- ✅ Sistema de cálculo inteligente implementado
- ✅ Painel administrativo configurado

## 🎯 Próximos Passos

### 1. Criar um Superusuário

```bash
python manage.py createsuperuser
```

Preencha:
- **Username**: seu_usuario
- **Email**: seu_email@exemplo.com
- **Password**: sua_senha (mínimo 8 caracteres)

### 2. Iniciar o Servidor

```bash
python manage.py runserver
```

### 3. Acessar o Sistema

Abra seu navegador e acesse:

- **Interface Principal**: http://127.0.0.1:8000/
- **Dashboard**: http://127.0.0.1:8000/dashboard/
- **Novo Orçamento**: http://127.0.0.1:8000/orcamentos/novo/
- **Painel Admin**: http://127.0.0.1:8000/admin/

## 📊 Dados Já Cadastrados

O sistema já possui:

- **8 Tipos de Material**: Tafetá, Sarja, Alta Definição, Dupla Densidade, Super Batidas, Canvas, Cetim, SuperSoft
- **9 Tipos de Corte**: Corte, Dobra Meio, Dobra Cantos, Corte Normal, Envelope, e mais
- **24 Preços**: Configurados para diferentes metragens (300 a 30.000 metros)
- **14 Coeficientes**: Para cálculo de valores baseados em largura
- **30 Texturas**: Pimentas, Folhas, Hibisco, Café, Flores, e muitas outras
- **Configurações**: Percentuais de ajuste já configurados

## 🎨 Testando o Sistema

### Criar um Orçamento de Teste

1. Acesse: http://127.0.0.1:8000/orcamentos/novo/

2. Preencha:
   - **Cliente**: Empresa Teste Ltda
   - **Tipo de Cliente**: Indústria Novo
   - **Tipo de Material**: Tafetá
   - **Largura**: 30 mm
   - **Comprimento**: 50 mm
   - **Tipo de Corte**: Corte Normal
   - **Quantidade de Metros**: 1000
   - **Quantidade de Unidades**: 5000

3. Observe os **valores sendo calculados em tempo real** enquanto você digita!

4. Clique em **Salvar Orçamento**

### Ver Dashboard

Acesse http://127.0.0.1:8000/dashboard/ para ver:
- Total de orçamentos
- Orçamentos do mês
- Valor total do mês
- Materiais mais utilizados
- Orçamentos recentes

## 🔧 Personalizando o Sistema

### Adicionar Novos Materiais

1. Acesse: http://127.0.0.1:8000/admin/orcamento/tipomaterial/
2. Clique em "Adicionar tipo de material"
3. Preencha nome, código e ordem
4. Salve

### Ajustar Preços

1. Acesse: http://127.0.0.1:8000/admin/orcamento/tabelapreco/
2. Edite os preços existentes ou adicione novos
3. Os cálculos serão atualizados automaticamente

### Modificar Coeficientes

1. Acesse: http://127.0.0.1:8000/admin/orcamento/coeficientefator/
2. Ajuste os coeficientes conforme necessário
3. Isso afetará diretamente os cálculos dos orçamentos

## 📱 Recursos Especiais

### Cálculo em Tempo Real

- Digite valores no formulário
- Veja os cálculos atualizarem **instantaneamente**
- Powered by HTMX + Alpine.js

### Interface Responsiva

- Funciona em desktop, tablet e celular
- Design moderno com Tailwind CSS
- Navegação intuitiva

### Sistema Inteligente

- Cálculos automáticos baseados em múltiplas variáveis
- Tabelas de preços dinâmicas
- Coeficientes personalizáveis
- Suporte a diferentes tipos de cliente

## 🎓 Entendendo os Cálculos

O sistema calcula os valores seguindo esta lógica:

1. **Preço Base**: Busca na tabela de preços baseado na metragem e material
2. **Coeficiente Fator**: Aplica baseado na largura e tipo de material
3. **Valor de Goma**: Adiciona se houver goma (fino/grosso/termocolante)
4. **Corte Especial**: Adiciona valores para Canvas ou Cetim
5. **CC (Coeficiente de Corte)**: Calcula baseado nas dimensões
6. **Percentual Ultrassônico**: Aplica 15% se houver corte ultrassônico
7. **Tipo de Cliente**: Aplica desconto/acréscimo conforme tipo
8. **Valores Finais**: Calcula metro, milheiro, unidade e total

## 💡 Dicas

- Use filtros na lista de orçamentos para encontrar rapidamente
- Consulte o dashboard para análises rápidas
- Edite configurações no admin para ajustes globais
- Experimente diferentes combinações para ver os cálculos

## 🐛 Resolução de Problemas

### Servidor não inicia

```bash
# Verifique se o ambiente virtual está ativado
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Reinstale as dependências
pip install -r requirements.txt
```

### Erro de importação

```bash
# Execute as migrações novamente
python manage.py migrate
```

### Valores não calculam

1. Verifique se há dados nas tabelas de preços
2. Verifique se há coeficientes cadastrados
3. Acesse o admin e confira as configurações

## 📞 Suporte

Para mais informações, consulte o README.md principal.

---

**Parabéns!** Você está pronto para usar o Sistema de Orçamentos! 🎉

