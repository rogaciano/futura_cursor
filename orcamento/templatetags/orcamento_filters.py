from django import template

register = template.Library()


@register.filter
def densidade(queryset, valor):
    """Filtra cores por densidade"""
    return queryset.filter(densidade=valor)


@register.filter
def sum_field(queryset, field_name):
    """Soma um campo específico de um queryset"""
    total = 0
    for obj in queryset:
        if hasattr(obj, field_name):
            value = getattr(obj, field_name)
            # Se for uma property ou método, chama
            if callable(value):
                value = value()
            total += value or 0
    return total


@register.filter
def pode_editar(orcamento, user):
    """Verifica se o usuário pode editar o orçamento"""
    if hasattr(orcamento, 'pode_editar') and callable(orcamento.pode_editar):
        return orcamento.pode_editar(user)
    return False

