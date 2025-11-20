"""
Views para gerenciamento de tabelas auxiliares (CRUD)
Menu: Tabelas
"""
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Count, Q
from .models import TipoMaterial, Batida, TabelaPreco, CoeficienteFator, ValorGoma, ValorCorte, Configuracao, Textura, TipoCorte
from .forms import TipoMaterialForm, BatidaForm


def is_gestor_or_superuser(user):
    """Verifica se o usuário é gestor ou superusuário"""
    return user.is_superuser or user.groups.filter(name='Gestor').exists()


class GestorRequiredMixin(UserPassesTestMixin):
    """Mixin para requerer que o usuário seja gestor ou superusuário"""
    def test_func(self):
        return is_gestor_or_superuser(self.request.user)
    
    def handle_no_permission(self):
        messages.error(self.request, 'Você não tem permissão para acessar esta área.')
        return redirect('orcamento:index')


@login_required
@user_passes_test(is_gestor_or_superuser)
def tabelas_index(request):
    """Dashboard principal do menu Tabelas"""
    
    # Estatísticas
    stats = {
        'tipos_material': TipoMaterial.objects.count(),
        'tipos_material_ativos': TipoMaterial.objects.filter(ativo=True).count(),
        'batidas': Batida.objects.count(),
        'batidas_ativas': Batida.objects.filter(ativo=True).count(),
        'tipos_corte': TipoCorte.objects.count(),
        'texturas': Textura.objects.count(),
        'tabelas_preco': TabelaPreco.objects.count(),
        'coeficientes': CoeficienteFator.objects.count(),
        'valores_goma': ValorGoma.objects.count(),
        'valores_corte': ValorCorte.objects.count(),
        'configuracoes': Configuracao.objects.count(),
    }
    
    # Materiais com contagem de batidas
    materiais_com_batidas = TipoMaterial.objects.annotate(
        total_batidas=Count('batidas')
    ).order_by('ordem', 'nome')[:10]
    
    context = {
        'stats': stats,
        'materiais_com_batidas': materiais_com_batidas,
    }
    
    return render(request, 'orcamento/tabelas/index.html', context)


# ================== TIPO MATERIAL ==================

class TipoMaterialListView(LoginRequiredMixin, GestorRequiredMixin, ListView):
    """Lista tipos de material"""
    model = TipoMaterial
    template_name = 'orcamento/tabelas/tipomaterial_list.html'
    context_object_name = 'materiais'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = TipoMaterial.objects.annotate(
            total_batidas=Count('batidas')
        ).order_by('ordem', 'nome')
        
        # Busca
        busca = self.request.GET.get('busca')
        if busca:
            queryset = queryset.filter(
                Q(nome__icontains=busca) | Q(codigo__icontains=busca)
            )
        
        # Filtro por status
        status = self.request.GET.get('status')
        if status == 'ativo':
            queryset = queryset.filter(ativo=True)
        elif status == 'inativo':
            queryset = queryset.filter(ativo=False)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['busca'] = self.request.GET.get('busca', '')
        context['status'] = self.request.GET.get('status', '')
        return context


class TipoMaterialCreateView(LoginRequiredMixin, GestorRequiredMixin, CreateView):
    """Criar novo tipo de material"""
    model = TipoMaterial
    template_name = 'orcamento/tabelas/tipomaterial_form.html'
    fields = ['nome', 'codigo', 'ordem', 'ativo']
    success_url = reverse_lazy('orcamento:tipomaterial_list')
    
    def form_valid(self, form):
        messages.success(self.request, f'Material "{form.instance.nome}" criado com sucesso!')
        return super().form_valid(form)


class TipoMaterialUpdateView(LoginRequiredMixin, GestorRequiredMixin, UpdateView):
    """Editar tipo de material"""
    model = TipoMaterial
    template_name = 'orcamento/tabelas/tipomaterial_form.html'
    fields = ['nome', 'codigo', 'ordem', 'ativo']
    success_url = reverse_lazy('orcamento:tipomaterial_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Incluir batidas do material
        context['batidas'] = self.object.batidas.all().order_by('ordem', 'numero_batidas')
        return context
    
    def form_valid(self, form):
        messages.success(self.request, f'Material "{form.instance.nome}" atualizado com sucesso!')
        return super().form_valid(form)


class TipoMaterialDeleteView(LoginRequiredMixin, GestorRequiredMixin, DeleteView):
    """Deletar tipo de material"""
    model = TipoMaterial
    template_name = 'orcamento/tabelas/tipomaterial_confirm_delete.html'
    success_url = reverse_lazy('orcamento:tipomaterial_list')
    
    def delete(self, request, *args, **kwargs):
        material = self.get_object()
        messages.success(request, f'Material "{material.nome}" deletado com sucesso!')
        return super().delete(request, *args, **kwargs)


# ================== BATIDAS ==================

class BatidaListView(LoginRequiredMixin, GestorRequiredMixin, ListView):
    """Lista batidas"""
    model = Batida
    template_name = 'orcamento/tabelas/batida_list.html'
    context_object_name = 'batidas'
    paginate_by = 30
    
    def get_queryset(self):
        queryset = Batida.objects.select_related('tipo_material').order_by(
            'tipo_material__ordem', 'tipo_material__nome', 'ordem', 'numero_batidas'
        )
        
        # Filtro por material
        material_id = self.request.GET.get('material')
        if material_id:
            queryset = queryset.filter(tipo_material_id=material_id)
        
        # Busca
        busca = self.request.GET.get('busca')
        if busca:
            queryset = queryset.filter(
                Q(tipo_material__nome__icontains=busca) |
                Q(descricao__icontains=busca) |
                Q(numero_batidas__icontains=busca)
            )
        
        # Filtro por status
        status = self.request.GET.get('status')
        if status == 'ativo':
            queryset = queryset.filter(ativo=True)
        elif status == 'inativo':
            queryset = queryset.filter(ativo=False)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['materiais'] = TipoMaterial.objects.filter(ativo=True).order_by('nome')
        context['material_id'] = self.request.GET.get('material', '')
        context['busca'] = self.request.GET.get('busca', '')
        context['status'] = self.request.GET.get('status', '')
        return context


class BatidaCreateView(LoginRequiredMixin, GestorRequiredMixin, CreateView):
    """Criar nova batida"""
    model = Batida
    template_name = 'orcamento/tabelas/batida_form.html'
    fields = ['tipo_material', 'numero_batidas', 'descricao', 'ordem', 'ativo']
    success_url = reverse_lazy('orcamento:batida_list')
    
    def form_valid(self, form):
        messages.success(
            self.request, 
            f'Batida "{form.instance.numero_batidas}" para {form.instance.tipo_material.nome} criada com sucesso!'
        )
        return super().form_valid(form)


class BatidaUpdateView(LoginRequiredMixin, GestorRequiredMixin, UpdateView):
    """Editar batida"""
    model = Batida
    template_name = 'orcamento/tabelas/batida_form.html'
    fields = ['tipo_material', 'numero_batidas', 'descricao', 'ordem', 'ativo']
    success_url = reverse_lazy('orcamento:batida_list')
    
    def form_valid(self, form):
        messages.success(
            self.request,
            f'Batida "{form.instance.numero_batidas}" atualizada com sucesso!'
        )
        return super().form_valid(form)


class BatidaDeleteView(LoginRequiredMixin, GestorRequiredMixin, DeleteView):
    """Deletar batida"""
    model = Batida
    template_name = 'orcamento/tabelas/batida_confirm_delete.html'
    success_url = reverse_lazy('orcamento:batida_list')
    
    def delete(self, request, *args, **kwargs):
        batida = self.get_object()
        messages.success(
            request,
            f'Batida "{batida.numero_batidas}" de {batida.tipo_material.nome} deletada com sucesso!'
        )
        return super().delete(request, *args, **kwargs)


# ================== QUICK ADD (AJAX) ==================

@login_required
@user_passes_test(is_gestor_or_superuser)
def batida_quick_add(request, material_id):
    """Adicionar batida rapidamente via AJAX"""
    if request.method == 'POST':
        material = get_object_or_404(TipoMaterial, id=material_id)
        numero_batidas = request.POST.get('numero_batidas')
        
        if numero_batidas:
            try:
                batida = Batida.objects.create(
                    tipo_material=material,
                    numero_batidas=int(numero_batidas),
                    ordem=material.batidas.count() + 1
                )
                messages.success(request, f'Batida {numero_batidas} adicionada ao {material.nome}!')
                return redirect('orcamento:tipomaterial_update', pk=material_id)
            except Exception as e:
                messages.error(request, f'Erro ao adicionar batida: {e}')
        else:
            messages.error(request, 'Número de batidas é obrigatório!')
    
    return redirect('orcamento:tipomaterial_update', pk=material_id)

