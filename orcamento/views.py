from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.db import models
from decimal import Decimal
import json
from .models import (
    Orcamento, TipoMaterial, TipoCorte, TabelaPreco,
    CoeficienteFator, ValorGoma, Textura, Vendedor, CorOrcamento
)
from .forms import OrcamentoForm


def login_view(request):
    """View de login"""
    if request.user.is_authenticated:
        return redirect('orcamento:index')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bem-vindo, {user.first_name or user.username}!')
                return redirect('orcamento:index')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'orcamento/login.html', {'form': form})


@login_required
def logout_view(request):
    """View de logout"""
    logout(request)
    messages.info(request, 'Você saiu do sistema.')
    return redirect('orcamento:login')


@login_required
def index(request):
    """Página inicial - redireciona baseado no tipo de usuário"""
    try:
        vendedor = request.user.vendedor
        if vendedor.is_gestor:
            return redirect('orcamento:dashboard_gestor')
        else:
            return redirect('orcamento:dashboard_vendedor')
    except Vendedor.DoesNotExist:
        # Se for superuser sem vendedor, vai para dashboard de gestor
        if request.user.is_superuser:
            return redirect('orcamento:dashboard_gestor')
        messages.error(request, 'Usuário não está vinculado a um vendedor.')
        return redirect('orcamento:login')


class OrcamentoListView(LoginRequiredMixin, ListView):
    """Lista de orçamentos - filtrada por vendedor se não for gestor"""
    model = Orcamento
    template_name = 'orcamento/orcamento_list.html'
    context_object_name = 'orcamentos'
    paginate_by = 20
    login_url = 'orcamento:login'
    
    def get_queryset(self):
        queryset = Orcamento.objects.filter(ativo=True).select_related(
            'tipo_material', 'tipo_corte', 'vendedor'
        ).order_by('-data_emissao')
        
        # Se não for gestor, mostra apenas seus orçamentos
        try:
            vendedor = self.request.user.vendedor
            if not vendedor.is_gestor:
                queryset = queryset.filter(vendedor=vendedor)
        except Vendedor.DoesNotExist:
            # Superuser vê tudo
            if not self.request.user.is_superuser:
                queryset = queryset.none()
        
        # Filtros
        cliente = self.request.GET.get('cliente')
        tipo_material = self.request.GET.get('tipo_material')
        vendedor_id = self.request.GET.get('vendedor')
        
        if cliente:
            queryset = queryset.filter(cliente__icontains=cliente)
        if tipo_material:
            queryset = queryset.filter(tipo_material_id=tipo_material)
        if vendedor_id:
            queryset = queryset.filter(vendedor_id=vendedor_id)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipos_material'] = TipoMaterial.objects.filter(ativo=True)
        
        # Se for gestor, mostra filtro de vendedores
        try:
            vendedor = self.request.user.vendedor
            if vendedor.is_gestor:
                context['vendedores'] = Vendedor.objects.filter(ativo=True)
                context['is_gestor'] = True
        except Vendedor.DoesNotExist:
            if self.request.user.is_superuser:
                context['vendedores'] = Vendedor.objects.filter(ativo=True)
                context['is_gestor'] = True
        
        return context


class OrcamentoCreateView(LoginRequiredMixin, CreateView):
    """Criar novo orçamento - vincula automaticamente ao vendedor logado"""
    model = Orcamento
    form_class = OrcamentoForm
    template_name = 'orcamento/orcamento_form.html'
    success_url = reverse_lazy('orcamento:orcamento_list')
    login_url = 'orcamento:login'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Novo Orçamento'
        context['tipos_material'] = TipoMaterial.objects.filter(ativo=True)
        context['tipos_corte'] = TipoCorte.objects.filter(ativo=True)
        context['texturas'] = Textura.objects.filter(ativo=True)
        return context
    
    def form_valid(self, form):
        # Vincula automaticamente ao vendedor logado
        try:
            vendedor = self.request.user.vendedor
            form.instance.vendedor = vendedor
        except Vendedor.DoesNotExist:
            if not self.request.user.is_superuser:
                messages.error(self.request, 'Usuário não está vinculado a um vendedor.')
                return redirect('orcamento:orcamento_list')
        
        # Salvar o orçamento primeiro
        response = super().form_valid(form)
        
        # Processar e salvar cores
        self._processar_cores(form.instance)
        
        # IMPORTANTE: Recalcular valores após salvar cores
        form.instance.calcular_valores()
        form.instance.save()
        
        messages.success(self.request, 'Orçamento criado com sucesso!')
        # Redireciona para a visualização do orçamento
        return redirect('orcamento:orcamento_detail', pk=form.instance.pk)
    
    def _processar_cores(self, orcamento):
        """Processa e salva as cores do orçamento"""
        cores_data = self.request.POST.get('cores_data', '{}')
        
        try:
            cores_json = json.loads(cores_data)
            
            # Remover cores antigas se estiver editando
            orcamento.cores.all().delete()
            
            # Salvar cores da 1ª densidade
            for i, cor in enumerate(cores_json.get('cores1', [])):
                if cor.get('codigo'):  # Só salva se tiver código
                    CorOrcamento.objects.create(
                        orcamento=orcamento,
                        posicao=cor.get('posicao', 'Fd'),
                        densidade='1',
                        codigo_cor=cor.get('codigo', ''),
                        quantidade_unidades=int(cor.get('unidades', 0)),
                        quantidade_demais=int(cor.get('demais', 0)),
                        ordem=i
                    )
            
            # Salvar cores da 2ª densidade (se for Dupla Densidade)
            if orcamento.is_dupla_densidade:
                for i, cor in enumerate(cores_json.get('cores2', [])):
                    if cor.get('codigo'):  # Só salva se tiver código
                        CorOrcamento.objects.create(
                            orcamento=orcamento,
                            posicao=cor.get('posicao', 'Fd'),
                            densidade='2',
                            codigo_cor=cor.get('codigo', ''),
                            quantidade_unidades=int(cor.get('unidades', 0)),
                            quantidade_demais=int(cor.get('demais', 0)),
                            ordem=i
                        )
        except (json.JSONDecodeError, ValueError) as e:
            # Log do erro mas não impede o salvamento do orçamento
            print(f"Erro ao processar cores: {e}")


class OrcamentoUpdateView(LoginRequiredMixin, UpdateView):
    """Editar orçamento - vendedor só edita seus próprios"""
    model = Orcamento
    form_class = OrcamentoForm
    template_name = 'orcamento/orcamento_form.html'
    success_url = reverse_lazy('orcamento:orcamento_list')
    login_url = 'orcamento:login'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Se não for gestor, só pode editar seus orçamentos
        try:
            vendedor = self.request.user.vendedor
            if not vendedor.is_gestor:
                queryset = queryset.filter(vendedor=vendedor)
        except Vendedor.DoesNotExist:
            if not self.request.user.is_superuser:
                queryset = queryset.none()
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Orçamento'
        context['tipos_material'] = TipoMaterial.objects.filter(ativo=True)
        context['tipos_corte'] = TipoCorte.objects.filter(ativo=True)
        context['texturas'] = Textura.objects.filter(ativo=True)
        
        # Adicionar cores existentes para carregar no formulário
        orcamento = self.object
        cores1 = list(orcamento.cores.filter(densidade='1').order_by('ordem').values(
            'posicao', 'codigo_cor', 'quantidade_unidades', 'quantidade_demais'
        ))
        cores2 = list(orcamento.cores.filter(densidade='2').order_by('ordem').values(
            'posicao', 'codigo_cor', 'quantidade_unidades', 'quantidade_demais'
        ))
        
        # Formatar para o formato esperado pelo Alpine.js
        context['cores1_json'] = json.dumps([{
            'posicao': c['posicao'],
            'codigo': c['codigo_cor'],
            'unidades': c['quantidade_unidades'],
            'demais': c['quantidade_demais']
        } for c in cores1]) if cores1 else '[]'
        
        context['cores2_json'] = json.dumps([{
            'posicao': c['posicao'],
            'codigo': c['codigo_cor'],
            'unidades': c['quantidade_unidades'],
            'demais': c['quantidade_demais']
        } for c in cores2]) if cores2 else '[]'
        
        # Adicionar dados de debug ao contexto
        from django.conf import settings
        if getattr(settings, 'DEBUG_CALCULOS', False):
            from .calculadora import CalculadoraOrcamento
            calculadora = CalculadoraOrcamento(orcamento)
            valores = calculadora.calcular()
            context['valores'] = valores  # Passa valores para preencher campos iniciais
            context['debug_calculos'] = True
        
        return context
    
    def form_valid(self, form):
        # Salvar o orçamento primeiro
        response = super().form_valid(form)
        
        # Processar e salvar cores
        self._processar_cores(form.instance)
        
        # IMPORTANTE: Recalcular valores após salvar cores
        form.instance.calcular_valores()
        form.instance.save()
        
        messages.success(self.request, 'Orçamento atualizado com sucesso!')
        # Redireciona para a visualização do orçamento
        return redirect('orcamento:orcamento_detail', pk=form.instance.pk)
    
    def _processar_cores(self, orcamento):
        """Processa e salva as cores do orçamento"""
        cores_data = self.request.POST.get('cores_data', '{}')
        
        try:
            cores_json = json.loads(cores_data)
            
            # Remover cores antigas
            orcamento.cores.all().delete()
            
            # Salvar cores da 1ª densidade
            for i, cor in enumerate(cores_json.get('cores1', [])):
                if cor.get('codigo'):  # Só salva se tiver código
                    CorOrcamento.objects.create(
                        orcamento=orcamento,
                        posicao=cor.get('posicao', 'Fd'),
                        densidade='1',
                        codigo_cor=cor.get('codigo', ''),
                        quantidade_unidades=int(cor.get('unidades', 0)),
                        quantidade_demais=int(cor.get('demais', 0)),
                        ordem=i
                    )
            
            # Salvar cores da 2ª densidade (se for Dupla Densidade)
            if orcamento.is_dupla_densidade:
                for i, cor in enumerate(cores_json.get('cores2', [])):
                    if cor.get('codigo'):  # Só salva se tiver código
                        CorOrcamento.objects.create(
                            orcamento=orcamento,
                            posicao=cor.get('posicao', 'Fd'),
                            densidade='2',
                            codigo_cor=cor.get('codigo', ''),
                            quantidade_unidades=int(cor.get('unidades', 0)),
                            quantidade_demais=int(cor.get('demais', 0)),
                            ordem=i
                        )
        except (json.JSONDecodeError, ValueError) as e:
            # Log do erro mas não impede o salvamento do orçamento
            print(f"Erro ao processar cores: {e}")


class OrcamentoDetailView(LoginRequiredMixin, DetailView):
    """Detalhes do orçamento - vendedor só vê seus próprios"""
    model = Orcamento
    template_name = 'orcamento/orcamento_detail.html'
    context_object_name = 'orcamento'
    login_url = 'orcamento:login'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Se não for gestor, só pode ver seus orçamentos
        try:
            vendedor = self.request.user.vendedor
            if not vendedor.is_gestor:
                queryset = queryset.filter(vendedor=vendedor)
        except Vendedor.DoesNotExist:
            if not self.request.user.is_superuser:
                queryset = queryset.none()
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Adicionar dados de debug se flag estiver ativa
        from django.conf import settings
        if getattr(settings, 'DEBUG_CALCULOS', False):
            from .calculadora import CalculadoraOrcamento
            calculadora = CalculadoraOrcamento(self.object)
            valores = calculadora.calcular()
            context['debug_info'] = valores.get('debug_info', {})
            context['debug_calculos'] = True
            
        return context


@login_required
def calcular_orcamento_ajax(request):
    """
    Endpoint AJAX/HTMX para calcular valores em tempo real
    """
    if request.method == 'POST':
        try:
            # Obter dados do formulário
            tipo_material_id = request.POST.get('tipo_material')
            largura_mm = int(request.POST.get('largura_mm', 0))
            comprimento_mm = int(request.POST.get('comprimento_mm', 0))
            quantidade_metros = int(request.POST.get('quantidade_metros', 0))
            quantidade_unidades = int(request.POST.get('quantidade_unidades', 0))
            tipo_corte_id = request.POST.get('tipo_corte')
            tem_goma = request.POST.get('tem_goma') == 'true'
            tipo_goma = request.POST.get('tipo_goma', '')
            tem_ultrassonico = request.POST.get('tem_ultrassonico') == 'true'
            tipo_cliente = request.POST.get('tipo_cliente', 'comercio_novo')
            
            # Criar objeto temporário para cálculo
            orcamento_temp = Orcamento(
                tipo_material_id=tipo_material_id,
                largura_mm=largura_mm,
                comprimento_mm=comprimento_mm,
                quantidade_metros=quantidade_metros,
                quantidade_unidades=quantidade_unidades,
                tipo_corte_id=tipo_corte_id,
                tem_goma=tem_goma,
                tipo_goma=tipo_goma if tem_goma else '',
                tem_ultrassonico=tem_ultrassonico,
                tipo_cliente=tipo_cliente,
            )
            
            # Calcular valores
            from .calculadora import CalculadoraOrcamento
            calculadora = CalculadoraOrcamento(orcamento_temp)
            valores = calculadora.calcular()
            
            # Preparar resposta
            response_data = {
                'success': True,
                'valor_metro': str(valores['valor_metro']),
                'valor_milheiro': str(valores['valor_milheiro']),
                'valor_unidade': str(valores['valor_unidade']),
                'valor_total': str(valores['valor_total']),
                'preco_base': str(valores['preco_base']),
                'coef_fator': str(valores['coef_fator']),
                'area_m2': str(valores['area_m2']),
                'debug_info': valores.get('debug_info', {}),
            }
            
            # Se for requisição HTMX, retornar HTML partial
            if request.htmx:
                from django.conf import settings
                return render(request, 'orcamento/partials/valores_calculados.html', {
                    'valores': valores,
                    'debug_calculos': getattr(settings, 'DEBUG_CALCULOS', False),
                })
            
            return JsonResponse(response_data)
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
    
    return JsonResponse({'success': False, 'error': 'Método não permitido'}, status=405)


@login_required
def obter_precos_material(request, material_id):
    """Retorna os preços disponíveis para um determinado material"""
    precos = TabelaPreco.objects.filter(
        tipo_material_id=material_id
    ).order_by('metragem').values('metragem', 'preco_metro')
    
    return JsonResponse(list(precos), safe=False)


def obter_batidas_material(request, material_id):
    """Retorna as batidas do material selecionado (primeira batida disponível)"""
    try:
        material = TipoMaterial.objects.get(id=material_id)
        batidas = material.batidas.filter(ativo=True).order_by('ordem', 'numero_batidas')
        
        if batidas.exists():
            primeira_batida = batidas.first()
            return JsonResponse({
                'batida_padrao': primeira_batida.numero_batidas,
                'descricao': primeira_batida.descricao,
                'nome_material': material.nome,
                'total_opcoes': batidas.count()
            })
        else:
            return JsonResponse({
                'batida_padrao': None,
                'descricao': 'Nenhuma batida configurada',
                'nome_material': material.nome,
                'total_opcoes': 0
            })
    except TipoMaterial.DoesNotExist:
        return JsonResponse({'error': 'Material não encontrado'}, status=404)


def obter_opcoes_batidas(request, material_id):
    """Retorna todas as opções de batidas para o material (para popular select)"""
    try:
        from .models import Batida
        batidas = Batida.objects.filter(
            tipo_material_id=material_id,
            ativo=True
        ).order_by('ordem', 'numero_batidas').values('id', 'numero_batidas', 'descricao')
        
        return JsonResponse(list(batidas), safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@login_required
def dashboard_vendedor(request):
    """Dashboard do vendedor - vê apenas seus dados"""
    from django.db.models import Sum, Count
    from datetime import datetime
    
    try:
        vendedor = request.user.vendedor
    except Vendedor.DoesNotExist:
        messages.error(request, 'Usuário não está vinculado a um vendedor.')
        return redirect('orcamento:login')
    
    hoje = datetime.now().date()
    mes_atual = hoje.replace(day=1)
    
    # Estatísticas do vendedor
    meus_orcamentos = Orcamento.objects.filter(vendedor=vendedor, ativo=True)
    
    context = {
        'vendedor': vendedor,
        'total_orcamentos': meus_orcamentos.count(),
        'orcamentos_mes': meus_orcamentos.filter(data_emissao__gte=mes_atual).count(),
        'valor_total_mes': meus_orcamentos.filter(
            data_emissao__gte=mes_atual
        ).aggregate(total=Sum('valor_total'))['total'] or Decimal('0.0'),
        'orcamentos_recentes': meus_orcamentos.order_by('-criado_em')[:10],
        'meta_mensal': vendedor.meta_mensal,
        'percentual_meta': vendedor.percentual_meta(),
    }
    
    return render(request, 'orcamento/dashboard_vendedor.html', context)


@login_required
def dashboard_gestor(request):
    """Dashboard do gestor - vê todos os dados"""
    from django.db.models import Sum, Count, Avg
    from datetime import datetime
    
    # Verificar se é gestor
    try:
        vendedor = request.user.vendedor
        if not vendedor.is_gestor and not request.user.is_superuser:
            messages.error(request, 'Acesso não autorizado.')
            return redirect('orcamento:dashboard_vendedor')
    except Vendedor.DoesNotExist:
        if not request.user.is_superuser:
            messages.error(request, 'Usuário não autorizado.')
            return redirect('orcamento:login')
    
    hoje = datetime.now().date()
    mes_atual = hoje.replace(day=1)
    
    context = {
        'total_orcamentos': Orcamento.objects.filter(ativo=True).count(),
        'orcamentos_mes': Orcamento.objects.filter(
            data_emissao__gte=mes_atual,
            ativo=True
        ).count(),
        'valor_total_mes': Orcamento.objects.filter(
            data_emissao__gte=mes_atual,
            ativo=True
        ).aggregate(total=Sum('valor_total'))['total'] or Decimal('0.0'),
        'orcamentos_recentes': Orcamento.objects.filter(
            ativo=True
        ).select_related('vendedor', 'tipo_material').order_by('-criado_em')[:10],
        'materiais_mais_usados': TipoMaterial.objects.annotate(
            total=Count('orcamento')
        ).order_by('-total')[:5],
        'vendedores_ranking': Vendedor.objects.filter(ativo=True).annotate(
            total_vendas=Sum('orcamentos__valor_total', filter=models.Q(
                orcamentos__data_emissao__gte=mes_atual,
                orcamentos__ativo=True
            )),
            qtd_orcamentos=Count('orcamentos', filter=models.Q(
                orcamentos__data_emissao__gte=mes_atual,
                orcamentos__ativo=True
            ))
        ).order_by('-total_vendas')[:10],
        'is_gestor': True,
    }
    
    return render(request, 'orcamento/dashboard_gestor.html', context)


# Mantém a view antiga de dashboard para compatibilidade
@login_required
def dashboard(request):
    """Redireciona para dashboard apropriado"""
    return index(request)
