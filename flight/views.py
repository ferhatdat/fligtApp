from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Flight, Reservation
from .serializers import FlightSerializer, ReservationSerializer, StaffFlightReservation
from rest_framework.permissions import IsAdminUser
from .permissions import IsStaffOrReadOnly
from datetime import datetime, date

class FlightView(ModelViewSet):

    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    permission_classes = [IsStaffOrReadOnly]

    def get_serializer_class(self):
        serializer = super().get_serializer_class()

        if self.request.user.is_staff:
            return StaffFlightReservation
        return serializer

    def get_queryset(self):
        now = datetime.now()
        current_time = now.strftime('%H:%M:%S')
        today = date.today()

        if self.request.user.is_staff:
            return super().get_queryset()
        else:
            queryset = Flight.objects.filter(date_of_departure__gt=today)

            if Flight.objects.filter(date_of_departure = today):

                today_qs = queryset.filter(etd__gt=current_time)

                queryset = queryset.union(today_qs)

                return queryset
            return queryset

class ReservationView(ModelViewSet):

    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.user.is_staff:
            return queryset
        return queryset.filter(user_id=self.request.user.id)
