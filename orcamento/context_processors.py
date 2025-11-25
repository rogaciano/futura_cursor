"""
Context processors para o app orcamento
"""
from django.conf import settings

def system_info(request):
    """
    Retorna informações gerais do sistema disponíveis em todos os templates
    """
    return {
        'SYSTEM_NAME': getattr(settings, 'SYSTEM_NAME', 'Futura Etiquetas'),
        'SYSTEM_VERSION': getattr(settings, 'SYSTEM_VERSION', '1.0.0'),
    }
