from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg, Count


class Destination(models.Model):
    name = models.CharField(
        unique=True,
        max_length=50,
        null=False,
        blank=False,
    )
    description = models.TextField(
        max_length=2000,
        null=False,
        blank=False,
    )
    # PT2: cada destino tiene su propia imagen
    image = models.ImageField(
        upload_to='destinations/',
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name

    # PT3: valoración media de las reviews de este destino
    def average_rating(self):
        result = self.reviews.aggregate(media=Avg('rating'))
        return result['media'] or 0

    def review_count(self):
        return self.reviews.count()


class Cruise(models.Model):
    name = models.CharField(
        unique=True,
        max_length=50,
        null=False,
        blank=False,
    )
    description = models.TextField(
        max_length=2000,
        null=False,
        blank=False,
    )
    destinations = models.ManyToManyField(
        Destination,
        related_name='cruises',
    )

    def __str__(self):
        return self.name

    # PT3: valoración media de las reviews de este crucero
    def average_rating(self):
        result = self.reviews.aggregate(media=Avg('rating'))
        return result['media'] or 0

    def review_count(self):
        return self.reviews.count()


class InfoRequest(models.Model):
    name = models.CharField(
        max_length=50,
        null=False,
        blank=False,
    )
    email = models.EmailField()
    notes = models.TextField(
        max_length=2000,
        null=False,
        blank=False,
    )
    cruise = models.ForeignKey(
        Cruise,
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return f'{self.name} - {self.cruise}'


class Booking(models.Model):
    """PT3: representa que un usuario ha comprado un crucero.
    Solo quien tiene un Booking puede dejar reviews."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookings',
    )
    cruise = models.ForeignKey(
        Cruise,
        on_delete=models.CASCADE,
        related_name='bookings',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'cruise')

    def __str__(self):
        return f'{self.user} -> {self.cruise}'


class Review(models.Model):
    """PT3: opinión sobre un destino O un crucero (uno de los dos)."""
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    comment = models.TextField(max_length=2000, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    destination = models.ForeignKey(
        Destination,
        on_delete=models.CASCADE,
        related_name='reviews',
        null=True,
        blank=True,
    )
    cruise = models.ForeignKey(
        Cruise,
        on_delete=models.CASCADE,
        related_name='reviews',
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        target = self.destination or self.cruise
        return f'{self.author} - {target} ({self.rating}/5)'
