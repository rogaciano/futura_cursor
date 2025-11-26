#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Ler o arquivo original
file_path = r'd:\projetos\futura_cursor\orcamento\templates\orcamento\orcamento_list.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Adicionar {% load orcamento_filters %} logo após {% extends 'base.html' %}
if '{% load orcamento_filters %}' not in content:
    content = content.replace(
        "{% extends 'base.html' %}",
        "{% extends 'base.html' %}\n{% load orcamento_filters %}"
    )

# 2. Adicionar dashboard de status após o header (antes de "<!-- Filtros -->")
dashboard_html = '''
    <!-- Dashboard de Status - Filtros Rápidos -->
    <div class="bg-white rounded-lg shadow-md p-6">
        <h2 class="text-lg font-semibold text-gray-800 mb-4">Filtrar por Status</h2>
        <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-8 gap-3">
            <!-- Digitando -->
            <a href="?status=digitando" class="bg-gray-50 hover:bg-gray-100 rounded-lg p-3 border-l-4 border-gray-400 transition group">
                <div class="text-center">
                    <p class="text-gray-600 text-xs font-medium uppercase mb-1">Digitando</p>
                    <p class="text-xl font-bold text-gray-700">{{ status_counts.digitando }}</p>
                </div>
            </a>

            <!-- Aguardando -->
            <a href="?status=aguardando" class="bg-yellow-50 hover:bg-yellow-100 rounded-lg p-3 border-l-4 border-yellow-400 transition group">
                <div class="text-center">
                    <p class="text-yellow-700 text-xs font-medium uppercase mb-1">Aguardando</p>
                    <p class="text-xl font-bold text-yellow-600">{{ status_counts.aguardando }}</p>
                </div>
            </a>

            <!-- Aprovado -->
            <a href="?status=aprovado" class="bg-green-50 hover:bg-green-100 rounded-lg p-3 border-l-4 border-green-400 transition group">
                <div class="text-center">
                    <p class="text-green-700 text-xs font-medium uppercase mb-1">Aprovado</p>
                    <p class="text-xl font-bold text-green-600">{{ status_counts.aprovado }}</p>
                </div>
            </a>

            <!-- Em Produção -->
            <a href="?status=em_producao" class="bg-blue-50 hover:bg-blue-100 rounded-lg p-3 border-l-4 border-blue-400 transition group">
                <div class="text-center">
                    <p class="text-blue-700 text-xs font-medium uppercase mb-1">Produção</p>
                    <p class="text-xl font-bold text-blue-600">{{ status_counts.em_producao }}</p>
                </div>
            </a>

            <!-- Finalizado -->
            <a href="?status=finalizado" class="bg-purple-50 hover:bg-purple-100 rounded-lg p-3 border-l-4 border-purple-400 transition group">
                <div class="text-center">
                    <p class="text-purple-700 text-xs font-medium uppercase mb-1">Finalizado</p>
                    <p class="text-xl font-bold text-purple-600">{{ status_counts.finalizado }}</p>
                </div>
            </a>

            <!-- Entregue -->
            <a href="?status=entregue" class="bg-teal-50 hover:bg-teal-100 rounded-lg p-3 border-l-4 border-teal-400 transition group">
                <div class="text-center">
                    <p class="text-teal-700 text-xs font-medium uppercase mb-1">Entregue</p>
                    <p class="text-xl font-bold text-teal-600">{{ status_counts.entregue }}</p>
                </div>
            </a>

            <!-- Cancelado -->
            <a href="?status=cancelado" class="bg-red-50 hover:bg-red-100 rounded-lg p-3 border-l-4 border-red-400 transition group">
                <div class="text-center">
                    <p class="text-red-700 text-xs font-medium uppercase mb-1">Cancelado</p>
                    <p class="text-xl font-bold text-red-600">{{ status_counts.cancelado }}</p>
                </div>
            </a>

            <!-- Reprovado -->
            <a href="?status=reprovado" class="bg-orange-50 hover:bg-orange-100 rounded-lg p-3 border-l-4 border-orange-400 transition group">
                <div class="text-center">
                    <p class="text-orange-700 text-xs font-medium uppercase mb-1">Reprovado</p>
                    <p class="text-xl font-bold text-orange-600">{{ status_counts.reprovado }}</p>
                </div>
            </a>
        </div>
    </div>

'''

# Adicionar dashboard antes de "<!-- Filtros -->" se ainda não existe
if 'Filtrar por Status' not in content:
    content = content.replace(
        '        <!-- Filtros -->',
        dashboard_html + '        <!-- Filtros -->'
    )

# 3. Corrigir linhas com {% if %} quebrado - Tipo de Material
content = content.replace(
    '''<option value="{{ material.id }}" {% if request.GET.tipo_material == material.id|stringformat:"s" %}selected{% endif %}>''',
    '''<option value="{{ material.id }}" {% if request.GET.tipo_material == material.id|stringformat:"s" %}selected{% endif %}>'''
)

# 4. Corrigir linhas com {% if %} quebrado - Vendedor
content = content.replace(
    '''<option value="{{ vendedor.id }}" {% if request.GET.vendedor == vendedor.id|stringformat:"s" %}selected{% endif %}>''',
    '''<option value="{{ vendedor.id }}" {% if request.GET.vendedor == vendedor.id|stringformat:"s" %}selected{% endif %}>'''
)

# 5. Adicionar coluna Status no header da tabela se não existe
if '"Status</th>' not in content:
    content = content.replace(
        '<th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-24">Pedido</th>\r\n                        <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Cliente</th>',
        '<th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-24">Pedido</th>\r\n                        <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>\r\n                        <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Cliente</th>'
    )

# 6. Adicionar célula Status no corpo da tabela
status_cell_insert = '''                        </td>
                        <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-500">
                            <span class="px-2 py-1 text-xs rounded-full font-semibold
                                {% if orcamento.status == 'digitando' %}bg-gray-100 text-gray-800
                                {% elif orcamento.status == 'aguardando' %}bg-yellow-100 text-yellow-800
                                {% elif orcamento.status == 'aprovado' %}bg-green-100 text-green-800
                                {% elif orcamento.status == 'em_producao' %}bg-blue-100 text-blue-800
                                {% elif orcamento.status == 'finalizado' %}bg-purple-100 text-purple-800
                                {% elif orcamento.status == 'entregue' %}bg-teal-100 text-teal-800
                                {% elif orcamento.status == 'cancelado' %}bg-red-100 text-red-800
                                {% elif orcamento.status == 'reprovado' %}bg-red-100 text-red-800
                                {% else %}bg-gray-100 text-gray-800{% endif %}">
                                {{ orcamento.get_status_display }}
                            </span>
                        </td>
                        <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">'''

if 'orcamento.get_status_display' not in content:
    # Encontrar e substituir primeira ocorrência após número do pedido
    import re
    pattern = r'(\{\{ orcamento\.numero_pedido\|default:"—" \}\}\r?\n\s*</td>\r?\n\s*<td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">)'
    content = re.sub(pattern, status_cell_insert, content, count=1)

# 7. Adicionar verificação de permissão usando o filtro pode_editar
edit_link_pattern = r'(<a href="\{% url \'orcamento:orcamento_update\' orcamento\.pk %\}"[^>]*>.*?</a>)'
if '|pode_editar:request.user' not in content:
    import re
    match = re.search(edit_link_pattern, content, re.DOTALL)
    if match:
        original_link = match.group(1)
        new_link = '''{% if orcamento|pode_editar:request.user %}
                                    ''' + original_link + '''
                                {% else %}
                                    <span class="text-gray-300 p-1.5 cursor-not-allowed" title="Bloqueado para edição">
                                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                                        </svg>
                                    </span>
                                {% endif %}'''
        content = content.replace(original_link, new_link)

# Salvar arquivo
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Arquivo corrigido com sucesso!")
print("   - {% load orcamento_filters %} adicionado")
print("   - Dashboard de status adicionado")
print("   - Coluna Status adicionada")
print("   - Filtro pode_editar adicionado")
