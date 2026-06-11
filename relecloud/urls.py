from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('destinations/', views.destinations, name='destinations'),
    path('destination/<int:pk>', views.DestinationDetailView.as_view(), name='destination_detail'),
    path('cruise/<int:pk>', views.CruiseDetailView.as_view(), name='cruise_detail'),
    path('info_request', views.InfoRequestCreate.as_view(), name='info_request'),
    # PT3: crear reviews
    path('cruise/<int:pk>/review', views.CreateCruiseReview.as_view(), name='cruise_review'),
    path('destination/<int:pk>/review', views.CreateDestinationReview.as_view(), name='destination_review'),
]
