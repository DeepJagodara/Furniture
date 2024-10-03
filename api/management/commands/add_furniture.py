from django.core.management.base import BaseCommand
from api.models import Furniture

class Command(BaseCommand):
    help = 'Adds a sample furniture item to the database'

    def handle(self, *args, **kwargs):
        Furniture.objects.create(
            name="Modern Sofa",
            description="A comfortable modern sofa.",
            price=499.99,
            available=True
        )
        self.stdout.write(self.style.SUCCESS('Successfully added furniture item'))
