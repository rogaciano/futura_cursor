from django.urls import path
from . import views
from . import views_tabelas

app_name = 'orcamento'

urlpatterns = [
    # Auth
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Home
    path('', views.index, name='index'),
    
    # Dashboards
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/vendedor/', views.dashboard_vendedor, name='dashboard_vendedor'),
    path('dashboard/gestor/', views.dashboard_gestor, name='dashboard_gestor'),
    
    # Orçamentos
    path('orcamentos/', views.OrcamentoListView.as_view(), name='orcamento_list'),
    path('orcamentos/novo/', views.OrcamentoCreateView.as_view(), name='orcamento_create'),
    path('orcamentos/<int:pk>/', views.OrcamentoDetailView.as_view(), name='orcamento_detail'),
    path('orcamentos/<int:pk>/editar/', views.OrcamentoUpdateView.as_view(), name='orcamento_update'),
    
    # Menu Tabelas - Dashboard
    path('tabelas/', views_tabelas.tabelas_index, name='tabelas_index'),
    
    # Tipo de Material (CRUD)
    path('tabelas/materiais/', views_tabelas.TipoMaterialListView.as_view(), name='tipomaterial_list'),
    path('tabelas/materiais/novo/', views_tabelas.TipoMaterialCreateView.as_view(), name='tipomaterial_create'),
    path('tabelas/materiais/<int:pk>/editar/', views_tabelas.TipoMaterialUpdateView.as_view(), name='tipomaterial_update'),
    path('tabelas/materiais/<int:pk>/deletar/', views_tabelas.TipoMaterialDeleteView.as_view(), name='tipomaterial_delete'),
    
    # Batidas (CRUD)
    path('tabelas/batidas/', views_tabelas.BatidaListView.as_view(), name='batida_list'),
    path('tabelas/batidas/novo/', views_tabelas.BatidaCreateView.as_view(), name='batida_create'),
    path('tabelas/batidas/<int:pk>/editar/', views_tabelas.BatidaUpdateView.as_view(), name='batida_update'),
    path('tabelas/batidas/<int:pk>/deletar/', views_tabelas.BatidaDeleteView.as_view(), name='batida_delete'),
    path('tabelas/batidas/add/<int:material_id>/', views_tabelas.batida_quick_add, name='batida_quick_add'),

    # Coeficientes Fator (CRUD)
    path('tabelas/coeficientes/', views_tabelas.CoeficienteFatorListView.as_view(), name='coeficientefator_list'),
    path('tabelas/coeficientes/novo/', views_tabelas.CoeficienteFatorCreateView.as_view(), name='coeficientefator_create'),
    path('tabelas/coeficientes/<int:pk>/editar/', views_tabelas.CoeficienteFatorUpdateView.as_view(), name='coeficientefator_update'),
    path('tabelas/coeficientes/<int:pk>/deletar/', views_tabelas.CoeficienteFatorDeleteView.as_view(), name='coeficientefator_delete'),
    
    # AJAX/HTMX endpoints
    path('api/calcular/', views.calcular_orcamento_ajax, name='calcular_ajax'),
    path('api/precos-material/<int:material_id>/', views.obter_precos_material, name='precos_material'),
    path('api/material/<int:material_id>/batidas/', views.obter_batidas_material, name='batidas_material'),
    path('api/material/<int:material_id>/opcoes-batidas/', views.obter_opcoes_batidas, name='opcoes_batidas'),
]

