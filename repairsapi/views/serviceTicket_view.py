"""View module for handling requests for customer data"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from repairsapi.models import ServiceTicket

class ServiceTicketView(ViewSet):
    """Honey Rae API ServiceTicket view"""

    def list(self, request):
        
        service_ticket = ServiceTicket.objects.all()
        serialized = ServiceTicketSerializer(service_ticket, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
            
            service_ticket = ServiceTicket.objects.get(pk=pk)
            serialized = ServiceTicketSerializer(service_ticket, context={'request': request})
            return Response(serialized.data, status=status.HTTP_200_OK)
    

class ServiceTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceTicket 
        fields = ('id', 'customer', 'employee', 'description', 'emergency', 'date_completed')
        depth = 1