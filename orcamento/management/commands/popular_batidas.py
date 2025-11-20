from django.core.management.base import BaseCommand
from orcamento.models import TipoMaterial, Batida


class Command(BaseCommand):
    help = 'Popula as batidas disponíveis para cada tipo de material'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Populando batidas por material...'))
        self.stdout.write('=' * 80)
        
        # Definir batidas para cada material
        # Formato: {codigo_material: [lista de números de batidas]}
        batidas_por_material = {
            'TAFETA': [20, 25, 28],
            'SARJA': [20, 25, 28],
            'ALTA_DEF': [20, 25, 30],
            'DUPLA_DENS': [20, 25, 28, 30],
            'SUPER_BAT': [25, 28, 30, 35],
            'CANVAS': [20, 25],
            'CETIM': [20, 25],
            'SUPERSOFT': [20, 25, 28],
        }
        
        total_criadas = 0
        total_atualizadas = 0
        
        for codigo_material, batidas_list in batidas_por_material.items():
            try:
                material = TipoMaterial.objects.get(codigo=codigo_material)
                self.stdout.write(f'\n{material.nome}:')
                
                for ordem, num_batidas in enumerate(batidas_list, 1):
                    batida, created = Batida.objects.update_or_create(
                        tipo_material=material,
                        numero_batidas=num_batidas,
                        defaults={
                            'descricao': f'{num_batidas} batidas',
                            'ordem': ordem,
                            'ativo': True
                        }
                    )
                    
                    if created:
                        self.stdout.write(f'  [+] Criada: {num_batidas} batidas')
                        total_criadas += 1
                    else:
                        self.stdout.write(f'  [~] Atualizada: {num_batidas} batidas')
                        total_atualizadas += 1
                        
            except TipoMaterial.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(f'  [!] Material {codigo_material} não encontrado')
                )
        
        self.stdout.write('\n' + '=' * 80)
        self.stdout.write(self.style.SUCCESS(f'Concluído!'))
        self.stdout.write(f'  Batidas criadas: {total_criadas}')
        self.stdout.write(f'  Batidas atualizadas: {total_atualizadas}')
        self.stdout.write(f'  Total de batidas: {Batida.objects.count()}')

