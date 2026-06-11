from django.contrib import admin
from . import models

admin.site.register(models.Cruise)
admin.site.register(models.Destination)
admin.site.register(models.InfoRequest)
admin.site.register(models.Booking)
admin.site.register(models.Review)
