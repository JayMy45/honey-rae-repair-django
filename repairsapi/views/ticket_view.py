"""View module for handling requests for customer data"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from repairsapi.models import ServiceTicket
from repairsapi.models import Employee
from repairsapi.models.customer import Customer

class ServiceTicketView(ViewSet):
    """Honey Rae API ServiceTicket view"""

    def create(self, request):
        """Handle POST requests for service tickets

        Returns:
            Response: JSON serialized representation of newly created service ticket
        """
        new_ticket = ServiceTicket()
        new_ticket.customer = Customer.objects.get(user=request.auth.user)
        new_ticket.description = request.data['description']
        new_ticket.emergency = request.data['emergency']
        new_ticket.save()

        serialized = ServiceTicketSerializer(new_ticket, many=False)

        return Response(serialized.data, status=status.HTTP_201_CREATED)
    
    def list(self, request):

        service_tickets = []

        if "status" in request.query_params:
            if request.query_params['status'] == "done":
                service_tickets = ServiceTicket.objects.filter(date_completed__isnull=False)

            if request.query_params['status'] == "all":
                service_tickets = ServiceTicket.objects.all()

        else:
            service_tickets = ServiceTicket.objects.all()


        serialized = ServiceTicketSerializer(service_tickets, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
            
            service_ticket = ServiceTicket.objects.get(pk=pk)
            serialized = ServiceTicketSerializer(service_ticket, context={'request': request})
            return Response(serialized.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        """Handles PUT request of single customer
        Returns: 
                Response - No response body status just (204) status
        """

        # Select the targeted ticket using pk
        ticket = ServiceTicket.objects.get(pk=pk)

        # Get the employee id from the client requests. employee is the key requested from client
        employee_id = request.data['employee']
       
        # Select the employee from the database using that id
        assigned_employee = Employee.objects.get(pk=employee_id)

        # Assign that Employee instance to the employee property of the ticket
        ticket.employee = assigned_employee

        # Save the updated ticket
        ticket.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)



    
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