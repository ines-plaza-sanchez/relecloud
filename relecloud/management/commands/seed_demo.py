"""Crea datos de demostración: destinos, cruceros, un usuario comprador y reviews.
Uso:  python manage.py seed_demo
Útil para la defensa oral y para poder probar PT3 (reviews) en la interfaz.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from relecloud.models import Destination, Cruise, Booking, Review


class Command(BaseCommand):
    help = 'Crea datos de demostración para ReleCloud'

    def handle(self, *args, **options):
        mars, _ = Destination.objects.get_or_create(
            name='Mars', defaults={'description': 'El planeta rojo.'})
        moon, _ = Destination.objects.get_or_create(
            name='Moon', defaults={'description': 'Nuestro satélite natural.'})

        cruise, _ = Cruise.objects.get_or_create(
            name='Mars Explorer', defaults={'description': 'Gran tour a Marte.'})
        cruise.destinations.add(mars, moon)

        buyer, created = User.objects.get_or_create(
            username='comprador', defaults={'email': 'comprador@relecloud.com'})
        if created:
            buyer.set_password('demo12345')
            buyer.save()

        Booking.objects.get_or_create(user=buyer, cruise=cruise)

        Review.objects.get_or_create(
            author=buyer, cruise=cruise,
            defaults={'rating': 5, 'comment': '¡Experiencia inolvidable!'})
        Review.objects.get_or_create(
            author=buyer, destination=mars,
            defaults={'rating': 4, 'comment': 'Marte es impresionante.'})

        self.stdout.write(self.style.SUCCESS(
            'Datos de demo creados. Usuario: comprador / demo12345'))
