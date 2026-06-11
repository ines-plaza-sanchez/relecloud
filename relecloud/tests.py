from django.test import TestCase
from django.urls import reverse
from django.core import mail

from .models import Destination, Cruise, InfoRequest


class PT1InfoRequestEmailTests(TestCase):
    """PT1 (TDD): enviar un correo real al recibir una solicitud de información."""

    def setUp(self):
        self.destination = Destination.objects.create(name='Mars', description='Red planet')
        self.cruise = Cruise.objects.create(name='Mars Explorer', description='Trip to Mars')
        self.cruise.destinations.add(self.destination)

    def test_submitting_info_request_sends_email(self):
        response = self.client.post(reverse('info_request'), {
            'name': 'Ana',
            'email': 'ana@example.com',
            'cruise': self.cruise.id,
            'notes': 'Quiero información',
        })
        self.assertEqual(response.status_code, 302)          # redirige tras guardar
        self.assertEqual(len(mail.outbox), 1)                # se ha enviado 1 correo
        self.assertIn('Ana', mail.outbox[0].body)
        self.assertIn('Mars Explorer', mail.outbox[0].body)

    def test_info_request_is_saved(self):
        self.client.post(reverse('info_request'), {
            'name': 'Ana',
            'email': 'ana@example.com',
            'cruise': self.cruise.id,
            'notes': 'Quiero información',
        })
        self.assertEqual(InfoRequest.objects.count(), 1)
