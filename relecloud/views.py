from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Avg, Count
from django.http import HttpResponseForbidden

from . import models
from .forms import ReviewForm


def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def destinations(request):
    # PT4: ordenar destinos por popularidad (nº de reviews y media)
    all_destinations = (
        models.Destination.objects
        .annotate(num_reviews=Count('reviews'), media=Avg('reviews__rating'))
        .order_by('-num_reviews', '-media', 'name')
    )
    return render(request, 'destinations.html', {'destinations': all_destinations})


class DestinationDetailView(generic.DetailView):
    template_name = 'destination_detail.html'
    model = models.Destination
    context_object_name = 'destination'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        destination = self.object
        context['reviews'] = destination.reviews.all()
        context['average_rating'] = destination.average_rating()
        context['review_form'] = ReviewForm()
        context['can_review'] = _user_can_review_destination(self.request.user, destination)
        return context


class CruiseDetailView(generic.DetailView):
    template_name = 'cruise_detail.html'
    model = models.Cruise
    context_object_name = 'cruise'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cruise = self.object
        context['reviews'] = cruise.reviews.all()
        context['average_rating'] = cruise.average_rating()
        context['review_form'] = ReviewForm()
        context['can_review'] = _user_can_review_cruise(self.request.user, cruise)
        return context


class InfoRequestCreate(SuccessMessageMixin, generic.CreateView):
    template_name = 'info_request_create.html'
    model = models.InfoRequest
    fields = ['name', 'email', 'cruise', 'notes']
    success_url = reverse_lazy('index')
    success_message = ('Thank you, %(name)s! We will email you when we have '
                       'more information about %(cruise)s!')

    def form_valid(self, form):
        # PT1: al recibir la solicitud, enviar un correo electrónico real
        response = super().form_valid(form)
        info_request = self.object
        send_mail(
            subject=f'Nueva solicitud de información de {info_request.name}',
            message=(
                f'Has recibido una nueva solicitud de información.\n\n'
                f'Nombre: {info_request.name}\n'
                f'Email: {info_request.email}\n'
                f'Crucero: {info_request.cruise}\n'
                f'Notas: {info_request.notes}\n'
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.INFO_REQUEST_RECIPIENT],
            fail_silently=False,
        )
        return response


# ----------------- PT3: lógica de permisos para reviews -----------------

def _user_can_review_cruise(user, cruise):
    """Solo usuarios autenticados que han comprado ese crucero."""
    if not user.is_authenticated:
        return False
    return models.Booking.objects.filter(user=user, cruise=cruise).exists()


def _user_can_review_destination(user, destination):
    """Solo usuarios autenticados que han comprado un crucero que visita ese destino."""
    if not user.is_authenticated:
        return False
    return models.Booking.objects.filter(
        user=user, cruise__destinations=destination
    ).exists()


class CreateCruiseReview(LoginRequiredMixin, generic.View):
    def post(self, request, pk):
        cruise = get_object_or_404(models.Cruise, pk=pk)
        if not _user_can_review_cruise(request.user, cruise):
            return HttpResponseForbidden(
                'Solo puedes opinar sobre cruceros que has comprado.'
            )
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.author = request.user
            review.cruise = cruise
            review.save()
            messages.success(request, '¡Gracias por tu opinión!')
        else:
            messages.error(request, 'Revisa los datos de tu opinión.')
        return redirect(reverse('cruise_detail', args=[pk]))


class CreateDestinationReview(LoginRequiredMixin, generic.View):
    def post(self, request, pk):
        destination = get_object_or_404(models.Destination, pk=pk)
        if not _user_can_review_destination(request.user, destination):
            return HttpResponseForbidden(
                'Solo puedes opinar sobre destinos que has visitado en un crucero comprado.'
            )
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.author = request.user
            review.destination = destination
            review.save()
            messages.success(request, '¡Gracias por tu opinión!')
        else:
            messages.error(request, 'Revisa los datos de tu opinión.')
        return redirect(reverse('destination_detail', args=[pk]))
