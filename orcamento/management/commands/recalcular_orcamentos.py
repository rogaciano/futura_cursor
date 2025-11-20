from django.core.management.base import BaseCommand
from orcamento.models import Orcamento
import traceback

class Command(BaseCommand):
    help = 'Recalcula todos os orçamentos existentes'

    def handle(self, *args, **options):
        self.stdout.write('Recalculando orcamentos...')
        self.stdout.write('=' * 60)
        
        orcamentos = Orcamento.objects.all()
        total = orcamentos.count()
        
        self.stdout.write(f'Encontrados {total} orcamentos')
        
        sucesso = 0
        erro = 0
        
        for i, orcamento in enumerate(orcamentos, 1):
            self.stdout.write(f'\n[{i}/{total}] Orcamento #{orcamento.id} - {orcamento.cliente}')
            self.stdout.write(f'  Antes: Total = R$ {orcamento.valor_total}, Unidades = {orcamento.quantidade_unidades}')
            
            try:
                # Recalcula valores
                orcamento.calcular_valores()
                orcamento.save()
                
                # Recarrega do banco
                orcamento.refresh_from_db()
                
                self.stdout.write(f'  Depois: Total = R$ {orcamento.valor_total}, Unidades = {orcamento.quantidade_unidades}')
                self.stdout.write(self.style.SUCCESS('  [OK] Recalculado com sucesso'))
                sucesso += 1
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'  [ERRO] {e}'))
                self.stdout.write(traceback.format_exc())
                erro += 1
        
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write(self.style.SUCCESS(f'\nConcluido!'))
        self.stdout.write(f'  Sucesso: {sucesso}')
        self.stdout.write(f'  Erros: {erro}')
