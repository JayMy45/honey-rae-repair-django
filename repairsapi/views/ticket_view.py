"""View module for handling requests for customer data"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from repairsapi.models import ServiceTicket, employee
from repairsapi.models import Employee
from repairsapi.models.customer import Customer

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
    
class TicketEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('id', 'specialty', 'full_name')

class TicketCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('id', 'full_name', 'address')

class ServiceTicketSerializer(serializers.ModelSerializer):
        # for the employee field I want to use the serializer; many equals false
    employee = TicketEmployeeSerializer(many=False)
    customer = TicketCustomerSerializer(many=False)
    
    class Meta:
        model = ServiceTicket 
        fields = ('id', 'description', 'emergency', 'date_completed', 'employee', 'customer' )
        depth = 1