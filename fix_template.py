import re

# Ler o arquivo
with open(r'd:\projetos\futura_cursor\orcamento\templates\orcamento\orcamento_list.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Adicionar coluna Status no cabeçalho (após Pedido)
content = content.replace(
    '<th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-24">Pedido</th>\r\n                        <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Cliente</th>',
    '<th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-24">Pedido</th>\r\n                        <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>\r\n                        <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Cliente</th>'
)

# 2. Adicionar célula de Status no corpo (após número do pedido)
status_cell = '''                        </td>
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

content = content.replace(
    '                        </td>\r\n                        <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">',
    status_cell,
    1  # Apenas a primeira ocorrência
)

# 3. Adicionar verificação de permissão de edição
content = content.replace(
    '''                                </a>
                                <a href="{% url 'orcamento:orcamento_update' orcamento.pk %}" 
                                   class="text-green-600 hover:text-green-800 p-1.5 rounded-full hover:bg-green-50 transition" title="Editar orçamento">
                                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                                    </svg>
                                </a>''',
    '''                                </a>
                                {% if orcamento|pode_editar:request.user %}
                                    <a href="{% url 'orcamento:orcamento_update' orcamento.pk %}" 
                                       class="text-green-600 hover:text-green-800 p-1.5 rounded-full hover:bg-green-50 transition" title="Editar orçamento">
                                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                                        </svg>
                                    </a>
                                {% else %}
                                    <span class="text-gray-300 p-1.5 cursor-not-allowed" title="Bloqueado para edição">
                                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                                        </svg>
                                    </span>
                                {% endif %}'''
)

# Salvar o arquivo
with open(r'd:\projetos\futura_cursor\orcamento\templates\orcamento\orcamento_list.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Arquivo corrigido com sucesso!")
