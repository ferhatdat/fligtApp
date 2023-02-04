from rest_framework import serializers
from .models import Flight, Reservation, Passenger

class FlightSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Flight
        fields = ('id', 'flight_number', 'operation_airlines', 'departure_city', 'arrival_city', 'date_of_departure', 'etd')

class PassengerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passenger
        fields = ('id', 'first_name', 'last_name', 'email', 'phone_number')

class ReservationSerializer(serializers.ModelSerializer):
    flight = serializers.StringRelatedField()
    flight_id = serializers.IntegerField()
    user = serializers.StringRelatedField()
    passenger = PassengerSerializer(many=True)
    class Meta:
        model = Reservation
        fields = ("id", "flight", "flight_id", "user", "passenger")

    def create(self, validated_data):
        passenger_data = validated_data.pop('passenger')
        validated_data['user_id']=self.context['request'].user.id
        reservation = Reservation.objects.create(**validated_data)

        for i in passenger_data:
            pas = Passenger.objects.create(**i)
            reservation.passenger.add(pas)
        reservation.save()
        return reservation
    
class StaffFlightReservation(serializers.ModelSerializer):
    reservation = ReservationSerializer(many=True, read_only=True )
    class Meta:
        model = Flight
        fields = ('id', 'flight_number', 'operation_airlines', 'departure_city', 'arrival_city', 'date_of_departure', 'etd', "reservation")
