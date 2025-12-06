import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
from ventas.models import User, Company, Customer, Interaction


class Command(BaseCommand):
    help = 'datos generados'

    def add_arguments(self, parser):
        parser.add_argument('users', type=int, default=3, help='Número de representantes')
        parser.add_argument('companies', type=int, default=50, help='Número de compañías')
        parser.add_argument('customers', type=int, default=1000, help='Número de clientes')
        parser.add_argument('interactions', type=int, default=500, help='Interacciones por cliente')

    def handle(self, *args, **options):
        fake = Faker('es_ES')
        num_users = options['users']
        num_companies = options['companies']
        num_customers = options['customers']
        num_interactions = options['interactions']
        
        self.stdout.write(f'Generando {num_users} users, {num_companies} companies, {num_customers} customers, {num_customers * num_interactions:,} interactions...\n')
        
        Interaction.objects.all().delete()
        Customer.objects.all().delete()
        Company.objects.all().delete()
        User.objects.all().delete()
        
        # representantes
        users = [User.objects.create(
            nombre=fake.name(),
            email=fake.unique.email(),
            password='password123',
            es_admin=(i == 0)
        ) for i in range(num_users)]
        self.stdout.write(f'{len(users)} representantes creados')
        
        # compañías
        companies = [Company.objects.create(nombre=fake.company()) for _ in range(num_companies)]
        self.stdout.write(f'{len(companies)} compañías creadas')
        
        # clientes
        customers = []
        for i in range(num_customers):
            customers.append(Customer.objects.create(
                nombre=fake.name(),
                fecha_nacimiento=fake.date_of_birth(minimum_age=18, maximum_age=80),
                empresa=random.choice(companies),
                representante=random.choice(users)
            ))
            if (i + 1) % 200 == 0:
                self.stdout.write(f'  → {i + 1} clientes')
        self.stdout.write(f'{len(customers)} clientes creados')
        
        # interacciones 
        self.stdout.write('Creando interacciones')
        tipos = ['Call', 'Email', 'SMS', 'Facebook', 'WhatsApp', 'LinkedIn', 'Meeting', 'Video Call']
        now = timezone.now()
        batch = []
        
        for i, customer in enumerate(customers):
            for _ in range(num_interactions):
                batch.append(Interaction(
                    cliente=customer,
                    tipo=random.choice(tipos),
                    fecha=now - timedelta(days=random.randint(0, 730), hours=random.randint(0, 23))
                ))
                
                if len(batch) >= 10000:
                    Interaction.objects.bulk_create(batch)
                    self.stdout.write(f'{(i * num_interactions) + len(batch):,} interacciones')
                    batch = []
            
            if (i + 1) % 100 == 0:
                self.stdout.write(f'Procesados {i + 1}/{num_customers} clientes')
        
        if batch:
            Interaction.objects.bulk_create(batch)
        
        self.stdout.write(self.style.SUCCESS(f'\n Datos generados: {User.objects.count()} users, {Company.objects.count()} companies, {Customer.objects.count()} customers, {Interaction.objects.count():,} interactions'))
