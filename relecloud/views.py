from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.conf import settings

from . import models


def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def destinations(request):
    all_destinations = models.Destination.objects.all()
    return render(request, 'destinations.html', {'destinations': all_destinations})


class DestinationDetailView(generic.DetailView):
    template_name = 'destination_detail.html'
    model = models.Destination
    context_object_name = 'destination'


class CruiseDetailView(generic.DetailView):
    template_name = 'cruise_detail.html'
    model = models.Cruise
    context_object_name = 'cruise'


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
