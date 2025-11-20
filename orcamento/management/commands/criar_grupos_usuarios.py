from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from orcamento.models import Vendedor, Orcamento
from decimal import Decimal


class Command(BaseCommand):
    help = 'Cria grupos (Vendedor e Gestor) e usuários de teste'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Criando grupos e permissões...'))
        
        # 1. Criar Grupos
        grupo_vendedor, created = Group.objects.get_or_create(name='Vendedor')
        if created:
            self.stdout.write('  [OK] Grupo "Vendedor" criado')
        else:
            self.stdout.write('  [INFO] Grupo "Vendedor" já existe')
        
        grupo_gestor, created = Group.objects.get_or_create(name='Gestor')
        if created:
            self.stdout.write('  [OK] Grupo "Gestor" criado')
        else:
            self.stdout.write('  [INFO] Grupo "Gestor" já existe')
        
        # 2. Configurar Permissões para Vendedor
        content_type = ContentType.objects.get_for_model(Orcamento)
        permissoes_vendedor = [
            Permission.objects.get(codename='add_orcamento', content_type=content_type),
            Permission.objects.get(codename='change_orcamento', content_type=content_type),
            Permission.objects.get(codename='view_orcamento', content_type=content_type),
        ]
        grupo_vendedor.permissions.set(permissoes_vendedor)
        self.stdout.write('  [OK] Permissões de Vendedor configuradas')
        
        # 3. Configurar Permissões para Gestor (todas)
        grupo_gestor.permissions.add(*permissoes_vendedor)
        grupo_gestor.permissions.add(
            Permission.objects.get(codename='delete_orcamento', content_type=content_type)
        )
        self.stdout.write('  [OK] Permissões de Gestor configuradas')
        
        # 4. Criar Usuários de Teste
        self.stdout.write('\nCriando usuários de teste...')
        
        # Vendedor 1
        user1, created = User.objects.get_or_create(
            username='vendedor1',
            defaults={
                'first_name': 'João',
                'last_name': 'Silva',
                'email': 'joao@example.com',
                'is_staff': True,
            }
        )
        if created:
            user1.set_password('vendedor123')
            user1.save()
            user1.groups.add(grupo_vendedor)
            
            Vendedor.objects.create(
                user=user1,
                nome_completo='João Silva',
                email='joao@example.com',
                telefone='(11) 98765-4321',
                comissao_percentual=Decimal('5.0'),
                meta_mensal=Decimal('10000.00')
            )
            self.stdout.write('  [OK] Vendedor "joao" criado')
            self.stdout.write('      Usuario: vendedor1')
            self.stdout.write('      Senha: vendedor123')
        else:
            self.stdout.write('  [INFO] Vendedor "vendedor1" já existe')
        
        # Vendedor 2
        user2, created = User.objects.get_or_create(
            username='vendedor2',
            defaults={
                'first_name': 'Maria',
                'last_name': 'Santos',
                'email': 'maria@example.com',
                'is_staff': True,
            }
        )
        if created:
            user2.set_password('vendedor123')
            user2.save()
            user2.groups.add(grupo_vendedor)
            
            Vendedor.objects.create(
                user=user2,
                nome_completo='Maria Santos',
                email='maria@example.com',
                telefone='(11) 98765-1234',
                comissao_percentual=Decimal('5.0'),
                meta_mensal=Decimal('12000.00')
            )
            self.stdout.write('  [OK] Vendedor "maria" criado')
            self.stdout.write('      Usuario: vendedor2')
            self.stdout.write('      Senha: vendedor123')
        else:
            self.stdout.write('  [INFO] Vendedor "vendedor2" já existe')
        
        # Gestor
        user_gestor, created = User.objects.get_or_create(
            username='gestor',
            defaults={
                'first_name': 'Carlos',
                'last_name': 'Pereira',
                'email': 'carlos@example.com',
                'is_staff': True,
            }
        )
        if created:
            user_gestor.set_password('gestor123')
            user_gestor.save()
            user_gestor.groups.add(grupo_gestor)
            
            Vendedor.objects.create(
                user=user_gestor,
                nome_completo='Carlos Pereira - Gestor',
                email='carlos@example.com',
                telefone='(11) 98765-9999',
                comissao_percentual=Decimal('0.0'),
                meta_mensal=Decimal('0.00')
            )
            self.stdout.write('  [OK] Gestor "carlos" criado')
            self.stdout.write('      Usuario: gestor')
            self.stdout.write('      Senha: gestor123')
        else:
            self.stdout.write('  [INFO] Gestor "gestor" já existe')
        
        # Resumo
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS('CONFIGURACAO CONCLUIDA!'))
        self.stdout.write('='*60)
        self.stdout.write('\nCredenciais de Acesso:')
        self.stdout.write('\n1. VENDEDOR 1:')
        self.stdout.write('   Usuario: vendedor1')
        self.stdout.write('   Senha: vendedor123')
        self.stdout.write('\n2. VENDEDOR 2:')
        self.stdout.write('   Usuario: vendedor2')
        self.stdout.write('   Senha: vendedor123')
        self.stdout.write('\n3. GESTOR:')
        self.stdout.write('   Usuario: gestor')
        self.stdout.write('   Senha: gestor123')
        self.stdout.write('\nTodos os usuários podem acessar:')
        self.stdout.write('http://127.0.0.1:8000/login/')
        self.stdout.write('\n')

