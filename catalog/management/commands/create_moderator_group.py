from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product


class Command(BaseCommand):
    help = 'Создаёт группу "Модератор продуктов" и назначает права'

    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(name='Модератор продуктов')

        # Право can_unpublish_product
        content_type = ContentType.objects.get_for_model(Product)
        perm = Permission.objects.get(content_type=content_type, codename='can_unpublish_product')
        group.permissions.add(perm)

        # Право на удаление продукта
        delete_perm = Permission.objects.get(content_type=content_type, codename='delete_product')
        group.permissions.add(delete_perm)

        group.save()
        self.stdout.write(self.style.SUCCESS('Группа "Модератор продуктов" создана и права назначены'))
