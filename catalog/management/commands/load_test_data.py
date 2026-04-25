from django.core.management import BaseCommand, call_command
from catalog.models import Product, Category


class Command(BaseCommand):
    help = 'Загружает тестовые данные в базу'

    def handle(self, *args, **options):
        # Очистка
        Product.objects.all().delete()
        Category.objects.all().delete()
        self.stdout.write('Старые данные удалены')

        # Загружаем фикстуры
        call_command('loaddata', 'categories.json')
        call_command('loaddata', 'products.json')

        self.stdout.write(self.style.SUCCESS('Тестовые данные загружены!'))
