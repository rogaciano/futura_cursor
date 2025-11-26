#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Ler o arquivo original
with open(r'd:\projetos\futura_cursor\orcamento\templates\orcamento\orcamento_list.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Criar lista de novas linhas
new_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    
    # 1. Adicionar {% load orcamento_filters %} após {% extends 'base.html' %}
    if i == 0 and '{% extends' in line:
        new_lines.append(line)
        new_lines.append('{% load orcamento_filters %}\r\n')
        i += 1
        continue
    
    # 2. Adicionar coluna Status no cabeçalho
    if '<th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-24">Pedido</th>' in line:
        new_lines.append(line)
        # Próxima linha deve ser Cliente, vamos adicionar Status antes
        i += 1
        if i < len(lines) and 'Cliente</th>' in lines[i]:
            new_lines.append('                        <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>\r\n')
            new_lines.append(lines[i])
            i += 1
            continue
    
    # 3. Adicionar célula Status no corpo (após número do pedido)
    if '{{ orcamento.numero_pedido|default:"—" }}' in line:
        new_lines.append(line)
        # Próximas linhas até encontrar a célula do cliente
        i += 1
        while i < len(lines) and '</td>' not in lines[i]:
            new_lines.append(lines[i])
            i += 1
        if i < len(lines):
            new_lines.append(lines[i])  # </td>
            i += 1
            # Adicionar célula de Status
            new_lines.append('                        <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-500">\r\n')
            new_lines.append('                            <span class="px-2 py-1 text-xs rounded-full font-semibold\r\n')
            new_lines.append('                                {% if orcamento.status == \'digitando\' %}bg-gray-100 text-gray-800\r\n')
            new_lines.append('                                {% elif orcamento.status == \'aguardando\' %}bg-yellow-100 text-yellow-800\r\n')
            new_lines.append('                                {% elif orcamento.status == \'aprovado\' %}bg-green-100 text-green-800\r\n')
            new_lines.append('                                {% elif orcamento.status == \'em_producao\' %}bg-blue-100 text-blue-800\r\n')
            new_lines.append('                                {% elif orcamento.status == \'finalizado\' %}bg-purple-100 text-purple-800\r\n')
            new_lines.append('                                {% elif orcamento.status == \'entregue\' %}bg-teal-100 text-teal-800\r\n')
            new_lines.append('                                {% elif orcamento.status == \'cancelado\' %}bg-red-100 text-red-800\r\n')
            new_lines.append('                                {% elif orcamento.status == \'reprovado\' %}bg-red-100 text-red-800\r\n')
            new_lines.append('                                {% else %}bg-gray-100 text-gray-800{% endif %}">\r\n')
            new_lines.append('                                {{ orcamento.get_status_display }}\r\n')
            new_lines.append('                            </span>\r\n')
            new_lines.append('                        </td>\r\n')
            continue
    
    # 4. Substituir link de edição por verificação de permissão
    if 'orcamento:orcamento_update' in line and '<a href=' in line:
        # Adicionar verificação de permissão
        new_lines.append('                                {% if orcamento|pode_editar:request.user %}\r\n')
        new_lines.append(line)
        # Continuar até fechar a tag </a>
        i += 1
        while i < len(lines) and '</a>' not in lines[i]:
            new_lines.append(lines[i])
            i += 1
        if i < len(lines):
            new_lines.append(lines[i])  # </a>
            i += 1
            # Adicionar else com ícone de bloqueado
            new_lines.append('                                {% else %}\r\n')
            new_lines.append('                                    <span class="text-gray-300 p-1.5 cursor-not-allowed" title="Bloqueado para edição">\r\n')
            new_lines.append('                                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">\r\n')
            new_lines.append('                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />\r\n')
            new_lines.append('                                        </svg>\r\n')
            new_lines.append('                                    </span>\r\n')
            new_lines.append('                                {% endif %}\r\n')
            continue
    
    new_lines.append(line)
    i += 1

# Salvar o arquivo
with open(r'd:\projetos\futura_cursor\orcamento\templates\orcamento\orcamento_list.html', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Template corrigido com sucesso!")
print(f"Total de linhas: {len(new_lines)}")
