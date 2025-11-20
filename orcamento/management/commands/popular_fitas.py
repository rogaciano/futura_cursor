from django.core.management.base import BaseCommand
from orcamento.models import Fita


class Command(BaseCommand):
    help = 'Popula a tabela de Fitas (fatores) com dados da planilha Plan2'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Populando tabela de Fitas...'))
        self.stdout.write('=' * 80)
        
        # Dados extraídos da Plan2 - Tabela FITAS
        # Largura (mm): Fator
        fitas_data = {
            10: 78.2,
            12: 67.0,
            15: 61.0,
            18: 47.6,
            20: 47.6,
            21: 45.4,
            24: 43.4,
            28: 38.3,
            30: 33.2,
            33: 33.2,
            40: 28.1,
            50: 23.0,
            67: 13.5,
            100: 11.5,
            200: 5.9,
        }
        
        total_criadas = 0
        total_atualizadas = 0
        
        for largura, fator in fitas_data.items():
            fita, created = Fita.objects.update_or_create(
                largura_mm=largura,
                defaults={
                    'fator': fator
                }
            )
            
            if created:
                self.stdout.write(f'  [+] Criada: {largura}mm -> Fator {fator}')
                total_criadas += 1
            else:
                self.stdout.write(f'  [~] Atualizada: {largura}mm -> Fator {fator}')
                total_atualizadas += 1
        
        self.stdout.write('\n' + '=' * 80)
        self.stdout.write(self.style.SUCCESS(f'Concluído!'))
        self.stdout.write(f'  Fitas criadas: {total_criadas}')
        self.stdout.write(f'  Fitas atualizadas: {total_atualizadas}')

