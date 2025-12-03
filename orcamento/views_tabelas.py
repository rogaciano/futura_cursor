"""
Views para gerenciamento de tabelas auxiliares (CRUD)
Menu: Tabelas
"""
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View, TemplateView
from django.db.models import Count, Q
from .models import TipoMaterial, Batida, TabelaPreco, CoeficienteFator, ValorGoma, ValorCorte, Configuracao, Textura, TipoCorte, Acabamento, PrecoAcabamento
from .forms import TipoMaterialForm, BatidaForm, CoeficienteFatorForm, TabelaPrecoForm
from .forms_tabelas import AcabamentoForm, PrecoAcabamentoForm
from .views_tabelas_pivot import AcabamentoPivotView
from .mixins import GestorRequiredMixin, is_gestor_or_superuser


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
        'acabamentos': Acabamento.objects.count(),
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
    fields = ['nome', 'codigo', 'ordem', 'dupla_densidade', 'ativo']
    success_url = reverse_lazy('orcamento:tipomaterial_list')
    
    def form_valid(self, form):
        messages.success(self.request, f'Material "{form.instance.nome}" criado com sucesso!')
        return super().form_valid(form)


class TipoMaterialUpdateView(LoginRequiredMixin, GestorRequiredMixin, UpdateView):
    """Editar tipo de material"""
    model = TipoMaterial
    template_name = 'orcamento/tabelas/tipomaterial_form.html'
    fields = ['nome', 'codigo', 'ordem', 'dupla_densidade', 'ativo']
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
    fields = ['tipo_material', 'numero_batidas', 'fator', 'descricao', 'ordem', 'ativo']
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
    fields = ['tipo_material', 'numero_batidas', 'fator', 'descricao', 'ordem', 'ativo']
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


# ================== COEFICIENTE FATOR ==================


class CoeficienteFatorListView(LoginRequiredMixin, GestorRequiredMixin, ListView):
    """Lista de coeficientes fator"""
    model = CoeficienteFator
    template_name = 'orcamento/tabelas/coeficientefator_list.html'
    context_object_name = 'coeficientes'
    paginate_by = 30

    def get_queryset(self):
        queryset = CoeficienteFator.objects.select_related('tipo_material', 'codigo_corte').order_by(
            'largura', 'tipo_material__nome', 'codigo_corte__nome'
        )

        material_id = self.request.GET.get('material')
        if material_id:
            queryset = queryset.filter(tipo_material_id=material_id)

        corte_id = self.request.GET.get('corte')
        if corte_id:
            queryset = queryset.filter(codigo_corte_id=corte_id)

        largura = self.request.GET.get('largura')
        if largura:
            queryset = queryset.filter(largura=largura)

        busca = self.request.GET.get('busca')
        if busca:
            queryset = queryset.filter(
                Q(tipo_material__nome__icontains=busca) |
                Q(codigo_corte__nome__icontains=busca)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['materiais'] = TipoMaterial.objects.order_by('nome')
        context['cortes'] = TipoCorte.objects.order_by('nome')
        context['material_id'] = self.request.GET.get('material', '')
        context['corte_id'] = self.request.GET.get('corte', '')
        context['largura'] = self.request.GET.get('largura', '')
        context['busca'] = self.request.GET.get('busca', '')
        return context


class CoeficienteFatorCreateView(LoginRequiredMixin, GestorRequiredMixin, CreateView):
    """Cria novo coeficiente"""
    model = CoeficienteFator
    form_class = CoeficienteFatorForm
    template_name = 'orcamento/tabelas/coeficientefator_form.html'
    success_url = reverse_lazy('orcamento:coeficientefator_list')

    def form_valid(self, form):
        messages.success(
            self.request,
            'Coeficiente criado com sucesso!'
        )
        return super().form_valid(form)


class CoeficienteFatorUpdateView(LoginRequiredMixin, GestorRequiredMixin, UpdateView):
    """Edita coeficiente"""
    model = CoeficienteFator
    form_class = CoeficienteFatorForm
    template_name = 'orcamento/tabelas/coeficientefator_form.html'
    success_url = reverse_lazy('orcamento:coeficientefator_list')

    def form_valid(self, form):
        messages.success(
            self.request,
            'Coeficiente atualizado com sucesso!'
        )
        return super().form_valid(form)


class CoeficienteFatorDeleteView(LoginRequiredMixin, GestorRequiredMixin, DeleteView):
    """Remove coeficiente"""
    model = CoeficienteFator
    template_name = 'orcamento/tabelas/coeficientefator_confirm_delete.html'
    success_url = reverse_lazy('orcamento:coeficientefator_list')

    def delete(self, request, *args, **kwargs):
        coef = self.get_object()
        messages.success(request, f'Coeficiente {coef} removido com sucesso!')
        return super().delete(request, *args, **kwargs)


# ================== TABELA DE PREÇO ==================

class TabelaPrecoListView(LoginRequiredMixin, GestorRequiredMixin, ListView):
    """Lista de tabelas de preço"""
    model = TabelaPreco
    template_name = 'orcamento/tabelas/tabelapreco_list.html'
    context_object_name = 'precos'
    paginate_by = 30

    def get_queryset(self):
        queryset = TabelaPreco.objects.select_related('tipo_material').order_by(
            'tipo_material__nome', 'metragem'
        )

        material_id = self.request.GET.get('material')
        if material_id:
            queryset = queryset.filter(tipo_material_id=material_id)

        busca = self.request.GET.get('busca')
        if busca:
            queryset = queryset.filter(
                Q(tipo_material__nome__icontains=busca) |
                Q(metragem__icontains=busca)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['materiais'] = TipoMaterial.objects.filter(ativo=True).order_by('nome')
        context['material_id'] = self.request.GET.get('material', '')
        context['busca'] = self.request.GET.get('busca', '')
        return context


class TabelaPrecoCreateView(LoginRequiredMixin, GestorRequiredMixin, CreateView):
    """Cria nova tabela de preço"""
    model = TabelaPreco
    form_class = TabelaPrecoForm
    template_name = 'orcamento/tabelas/tabelapreco_form.html'
    success_url = reverse_lazy('orcamento:tabelapreco_list')

    def form_valid(self, form):
        messages.success(
            self.request,
            'Preço criado com sucesso!'
        )
        return super().form_valid(form)


class TabelaPrecoUpdateView(LoginRequiredMixin, GestorRequiredMixin, UpdateView):
    """Edita tabela de preço"""
    model = TabelaPreco
    form_class = TabelaPrecoForm
    template_name = 'orcamento/tabelas/tabelapreco_form.html'
    success_url = reverse_lazy('orcamento:tabelapreco_list')

    def form_valid(self, form):
        messages.success(
            self.request,
            'Preço atualizado com sucesso!'
        )
        return super().form_valid(form)


class TabelaPrecoDeleteView(LoginRequiredMixin, GestorRequiredMixin, DeleteView):
    """Remove tabela de preço"""
    model = TabelaPreco
    template_name = 'orcamento/tabelas/tabelapreco_confirm_delete.html'
    success_url = reverse_lazy('orcamento:tabelapreco_list')

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(request, f'Preço de {obj.metragem}m para {obj.tipo_material.nome} removido!')
        return super().delete(request, *args, **kwargs)


class TabelaPrecoCopyView(LoginRequiredMixin, GestorRequiredMixin, View):
    """Copia preços de um material para outro"""
    
    def post(self, request, *args, **kwargs):
        source_id = request.POST.get('source_material')
        dest_id = request.POST.get('dest_material')
        
        if not source_id or not dest_id:
            messages.error(request, 'Selecione os materiais de origem e destino.')
            return redirect('orcamento:tabelapreco_list')
        
        if source_id == dest_id:
            messages.error(request, 'Os materiais de origem e destino devem ser diferentes.')
            return redirect('orcamento:tabelapreco_list')
            
        try:
            source_material = TipoMaterial.objects.get(pk=source_id)
            dest_material = TipoMaterial.objects.get(pk=dest_id)
            
            source_precos = TabelaPreco.objects.filter(tipo_material=source_material)
            
            if not source_precos.exists():
                messages.warning(request, f'Não há preços cadastrados para {source_material.nome}.')
                return redirect('orcamento:tabelapreco_list')
            
            count_created = 0
            count_updated = 0
            
            for preco in source_precos:
                obj, created = TabelaPreco.objects.update_or_create(
                    tipo_material=dest_material,
                    metragem=preco.metragem,
                    defaults={'preco_metro': preco.preco_metro}
                )
                if created:
                    count_created += 1
                else:
                    count_updated += 1
            
            messages.success(
                request, 
                f'Cópia concluída! {count_created} criados, {count_updated} atualizados para {dest_material.nome}.'
            )
            
        except TipoMaterial.DoesNotExist:
            messages.error(request, 'Material não encontrado.')
        except Exception as e:
            messages.error(request, f'Erro ao copiar: {e}')
            
        return redirect('orcamento:tabelapreco_list')


class TabelaPrecoPivotView(LoginRequiredMixin, GestorRequiredMixin, TemplateView):
    """Visão pivot da tabela de preços (Materiais x Metragens)"""
    template_name = 'orcamento/tabelas/tabelapreco_pivot.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Buscar todas as metragens únicas, ordenadas
        metragens = list(TabelaPreco.objects.values_list('metragem', flat=True)
                         .distinct().order_by('metragem'))
        
        # Buscar todos os materiais ativos, ordenados
        materiais = TipoMaterial.objects.filter(ativo=True).order_by('ordem', 'nome')
        
        # Montar a estrutura de dados para a tabela pivot
        # [
        #   {
        #     'material': material_obj,
        #     'precos': {metragem: preco, ...}
        #   },
        #   ...
        # ]
        
        pivot_data = []
        
        for material in materiais:
            # Buscar preços deste material
            precos = TabelaPreco.objects.filter(tipo_material=material)
            precos_map = {p.metragem: p.preco_metro for p in precos}
            
            row = {
                'material': material,
                'precos': []
            }
            
            # Preencher a lista de preços na ordem das colunas de metragens
            for m in metragens:
                valor = precos_map.get(m)
                row['precos'].append({
                    'metragem': m,
                    'valor': valor,
                    'existe': valor is not None
                })
                
            pivot_data.append(row)
            
        context['metragens'] = metragens
        context['pivot_data'] = pivot_data
        
        return context


# ================== ACABAMENTOS ==================

class AcabamentoListView(LoginRequiredMixin, GestorRequiredMixin, ListView):
    """Lista acabamentos"""
    model = Acabamento
    template_name = 'orcamento/tabelas/acabamento_list.html'
    context_object_name = 'acabamentos'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Acabamento.objects.order_by('ordem', 'nome')
        
        busca = self.request.GET.get('busca')
        if busca:
            queryset = queryset.filter(
                Q(nome__icontains=busca) | Q(codigo__icontains=busca)
            )
        
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


class AcabamentoCreateView(LoginRequiredMixin, GestorRequiredMixin, CreateView):
    """Criar novo acabamento"""
    model = Acabamento
    form_class = AcabamentoForm
    template_name = 'orcamento/tabelas/acabamento_form.html'
    success_url = reverse_lazy('orcamento:acabamento_list')
    
    def form_valid(self, form):
        messages.success(self.request, f'Acabamento "{form.instance.nome}" criado com sucesso!')
        return super().form_valid(form)


class AcabamentoUpdateView(LoginRequiredMixin, GestorRequiredMixin, UpdateView):
    """Editar acabamento"""
    model = Acabamento
    form_class = AcabamentoForm
    template_name = 'orcamento/tabelas/acabamento_form.html'
    success_url = reverse_lazy('orcamento:acabamento_list')
    
    def form_valid(self, form):
        messages.success(self.request, f'Acabamento "{form.instance.nome}" atualizado com sucesso!')
        return super().form_valid(form)


class AcabamentoDeleteView(LoginRequiredMixin, GestorRequiredMixin, DeleteView):
    """Deletar acabamento"""
    model = Acabamento
    template_name = 'orcamento/tabelas/acabamento_confirm_delete.html'
    success_url = reverse_lazy('orcamento:acabamento_list')
    
    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(request, f'Acabamento "{obj.nome}" deletado com sucesso!')
        return super().delete(request, *args, **kwargs)


# ================== PREÇOS DE ACABAMENTO ==================

class PrecoAcabamentoCreateView(LoginRequiredMixin, GestorRequiredMixin, View):
    """Criar preço de acabamento (via modal na tela de edição)"""
    
    def post(self, request, acabamento_id):
        acabamento = get_object_or_404(Acabamento, pk=acabamento_id)
        
        try:
            PrecoAcabamento.objects.create(
                acabamento=acabamento,
                largura_mm=request.POST.get('largura_mm'),
                preco=request.POST.get('preco')
            )
            messages.success(request, 'Preço adicionado com sucesso!')
        except Exception as e:
            messages.error(request, f'Erro ao adicionar preço: {e}')
            
        return redirect('orcamento:acabamento_update', pk=acabamento_id)


class PrecoAcabamentoDeleteView(LoginRequiredMixin, GestorRequiredMixin, DeleteView):
    """Deletar preço de acabamento"""
    model = PrecoAcabamento
    
    def delete(self, request, *args, **kwargs):
        preco = self.get_object()
        acabamento_id = preco.acabamento.id
        preco.delete()
        messages.success(request, 'Preço removido com sucesso!')
        return redirect('orcamento:acabamento_update', pk=acabamento_id)
