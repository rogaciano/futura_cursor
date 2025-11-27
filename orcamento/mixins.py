from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import redirect

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

