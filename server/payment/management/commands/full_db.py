import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from faker import Faker

from server.payment.choices import ReasonChoices
from server.payment.models import Collect

User = get_user_model()
fake = Faker('ru_RU')


class Command(BaseCommand):
    """Class for full_db command."""

    help = 'Full DB test-data.'

    def add_arguments(self, parser):
        """Method for adding optional args."""
        parser.add_argument(
            '--users', type=int, default=10, help='Count of users'
        )
        parser.add_argument(
            '--collects', type=int, default=5, help='Count of collects'
        )
        parser.add_argument(
            '--payments', type=int, default=50, help='Count of payments'
        )
        parser.add_argument(
            '--flush', action='store_true', help='Delete db'
        )

    def handle(self, *args, **options):
        """Main logic of full_db command."""
        users_count = options['users']
        collects_count = options['collects']
        payments_count = options['payments']
        flush = options['flush']
        if flush:
            self.stdout.write('🗑 Delete previous data...')
            User.objects.all().delete()
            Collect.objects.all().delete()

        self.stdout.write('👤 Сreate users...')
        users = [
            User.objects.create_user(
                username=fake.user_name() + str(i),
                email=fake.email(),
                password='123456',
            )
            for i in range(users_count)
        ]
        self.stdout.write('📦 Create collects...')
        collects = []
        for i in range(collects_count):
            user = random.choice(users)
            collect = Collect.objects.create(
                user=user,
                title=fake.sentence(nb_words=3),
                reason=random.choice(ReasonChoices.values),
                description=fake.text(max_nb_chars=200),
                target_amount=random.choice(
                    [None, random.randint(5000, 20000)]
                ),
                current_amount=0,
                donators_count=0,
            )
            collects.append(collect)

        self.stdout.write('💰 Create payments...')
        for _ in range(payments_count):
            user = random.choice(users)
            collect = random.choice(collects)
            collect.add_payment(
                user=user,
                amount=random.randint(100, 2000),
                comment=fake.sentence(nb_words=6),
            )

        self.stdout.write(self.style.SUCCESS(
            '✅ Database was updated and fulled new data!'
        ))
