     1|"""
     2|Context processors para o app orcamento
     3|"""
     4|from django.conf import settings
     5|
     6|def system_info(request):
     7|    """
     8|    Retorna informações gerais do sistema disponíveis em todos os templates
     9|    """
    10|    return {
    11|        'SYSTEM_NAME': getattr(settings, 'SYSTEM_NAME', 'Futura Etiquetas'),
    12|        'SYSTEM_VERSION': getattr(settings, 'SYSTEM_VERSION', '1.0.0'),
    13|    }
    14|
