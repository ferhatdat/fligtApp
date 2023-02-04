from django.contrib import admin
from django.urls import path, include
from .views import FlightView, ReservationView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'flight', FlightView)
router.register(r'reservation', ReservationView)

urlpatterns = [
    path('', include(router.urls)),
]