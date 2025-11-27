from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from .mixins import GestorRequiredMixin
from .models import Acabamento, PrecoAcabamento

class AcabamentoPivotView(LoginRequiredMixin, GestorRequiredMixin, TemplateView):
    """Visão pivot de acabamentos (Materiais x Larguras)"""
    template_name = 'orcamento/tabelas/acabamento_pivot.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Buscar todas as larguras únicas, ordenadas
        larguras = list(PrecoAcabamento.objects.values_list('largura_mm', flat=True)
                         .distinct().order_by('largura_mm'))
        
        # Buscar todos os acabamentos ativos, ordenados
        acabamentos = Acabamento.objects.filter(ativo=True).order_by('ordem', 'nome')
        
        # Montar a estrutura de dados para a tabela pivot
        # [
        #   {
        #     'acabamento': acabamento_obj,
        #     'precos': {largura_mm: preco, ...}
        #   },
        #   ...
        # ]
        
        pivot_data = []
        
        for acabamento in acabamentos:
            # Buscar preços deste acabamento
            precos = PrecoAcabamento.objects.filter(acabamento=acabamento)
            precos_map = {p.largura_mm: p.preco for p in precos}
            
            row = {
                'acabamento': acabamento,
                'precos': []
            }
            
            # Preencher a lista de preços na ordem das colunas de larguras
            for l in larguras:
                valor = precos_map.get(l)
                row['precos'].append({
                    'largura_mm': l,
                    'valor': valor,
                    'existe': valor is not None
                })
                
            pivot_data.append(row)
            
        context['larguras'] = larguras
        context['pivot_data'] = pivot_data
        
        return context
