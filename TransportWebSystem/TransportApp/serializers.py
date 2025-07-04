from rest_framework import serializers
from TransportApp.models import TransportOrder, Waypoint

class WaypointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Waypoint
        fields = ['location_name', 'waypoint_type']

class TransportOrderSerializer(serializers.ModelSerializer):
    waypoints = WaypointSerializer(many=True)

    class Meta:
        model = TransportOrder
        fields = ['id', 'order_number', 'customer_name', 'date', 'waypoints']

    def create(self, validated_data):
        waypoints_data = validated_data.pop('waypoints')
        order = TransportOrder.objects.create(**validated_data)
        for waypoint in waypoints_data:
            Waypoint.objects.create(transport_order=order, **waypoint)
        return order

    def update(self, instance, validated_data):
        waypoints_data = validated_data.pop('waypoints')

        instance.order_number = validated_data.get('order_number', instance.order_number)
        instance.customer_name = validated_data.get('customer_name', instance.customer_name)
        instance.date = validated_data.get('date', instance.date)
        instance.save()

        instance.waypoints.all().delete()

        for waypoint in waypoints_data:
            Waypoint.objects.create(transport_order=instance, **waypoint)

        return instance
