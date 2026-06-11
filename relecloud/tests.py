from django.test import TestCase
from django.urls import reverse
from django.core import mail
from django.contrib.auth.models import User

from .models import Destination, Cruise, InfoRequest, Booking, Review


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


class PT2DestinationImageTests(TestCase):
    """PT2 (funcional): el modelo Destination admite una imagen propia."""

    def test_destination_has_image_field(self):
        field_names = [f.name for f in Destination._meta.get_fields()]
        self.assertIn('image', field_names)

    def test_destination_image_can_be_blank(self):
        # Debe poder crearse sin imagen (campo opcional) sin lanzar error
        d = Destination.objects.create(name='Moon', description='Our satellite')
        self.assertFalse(bool(d.image))


class PT3ReviewTests(TestCase):
    """PT3 (TDD): reviews restringidas a compradores y valoración media."""

    def setUp(self):
        self.destination = Destination.objects.create(name='Mars', description='Red planet')
        self.cruise = Cruise.objects.create(name='Mars Explorer', description='Trip to Mars')
        self.cruise.destinations.add(self.destination)
        self.buyer = User.objects.create_user('buyer', password='pass12345')
        self.other = User.objects.create_user('other', password='pass12345')
        Booking.objects.create(user=self.buyer, cruise=self.cruise)

    def test_buyer_can_review_cruise(self):
        self.client.login(username='buyer', password='pass12345')
        response = self.client.post(
            reverse('cruise_review', args=[self.cruise.id]),
            {'rating': 5, 'comment': 'Increíble'},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Review.objects.filter(cruise=self.cruise).count(), 1)

    def test_non_buyer_cannot_review_cruise(self):
        self.client.login(username='other', password='pass12345')
        response = self.client.post(
            reverse('cruise_review', args=[self.cruise.id]),
            {'rating': 5, 'comment': 'No debería poder'},
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Review.objects.count(), 0)

    def test_anonymous_cannot_review_cruise(self):
        response = self.client.post(
            reverse('cruise_review', args=[self.cruise.id]),
            {'rating': 5, 'comment': 'Anónimo'},
        )
        # LoginRequiredMixin redirige al login
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Review.objects.count(), 0)

    def test_buyer_can_review_destination_of_purchased_cruise(self):
        self.client.login(username='buyer', password='pass12345')
        response = self.client.post(
            reverse('destination_review', args=[self.destination.id]),
            {'rating': 4, 'comment': 'Bonito'},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Review.objects.filter(destination=self.destination).count(), 1)

    def test_average_rating_is_computed(self):
        Review.objects.create(author=self.buyer, cruise=self.cruise, rating=4)
        Review.objects.create(author=self.other, cruise=self.cruise, rating=2)
        self.assertEqual(self.cruise.average_rating(), 3)

    def test_average_rating_zero_without_reviews(self):
        self.assertEqual(self.destination.average_rating(), 0)
