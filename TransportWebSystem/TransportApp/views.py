from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from TransportApp.models import TransportOrder, Waypoint
from TransportApp.serializers import TransportOrderSerializer, WaypointSerializer

# Create your views here.

@csrf_exempt
def transportorderApi(request, id=0):
    if request.method == 'GET':
        if id > 0:
            try:
                order = TransportOrder.objects.get(pk=id)
                serializer = TransportOrderSerializer(order)
                return JsonResponse(serializer.data, safe=False)
            except TransportOrder.DoesNotExist:
                return JsonResponse({'error': 'TransportOrder not found'}, status=404)
        else:
            orders = TransportOrder.objects.all()
            serializer = TransportOrderSerializer(orders, many=True)
            return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = TransportOrderSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        try:
            order = TransportOrder.objects.get(pk=id)
        except TransportOrder.DoesNotExist:
            return JsonResponse({'error': 'TransportOrder not found'}, status=404)
        
        serializer = TransportOrderSerializer(order, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        try:
            order = TransportOrder.objects.get(pk=id)
        except TransportOrder.DoesNotExist:
            return JsonResponse({'error': 'TransportOrder not found'}, status=404)
        order.delete()
        return JsonResponse({'message': 'TransportOrder deleted successfully'}, status=204)