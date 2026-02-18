from .models import Customer, Order, Remission, Sale, CreditAssignment
from .serializers import CustomerSerializer, OrderSerializer, RemissionSerializer, SaleSerializer, CreditAssignmentSerializer
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from django.db.models import Sum, F, Count
from django.db.models.functions import TruncDate
from django.utils.dateparse import parse_date
from django.utils import timezone
from datetime import datetime, time

class CustomerViewSet( viewsets.ModelViewSet ):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.AllowAny]

class OrderViewSet( viewsets.ModelViewSet ):
    queryset = Order.objects.select_related('customer').all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.AllowAny]

class RemissionViewSet( viewsets.ModelViewSet ):
    queryset = Remission.objects.select_related('order').prefetch_related('sales', 'credits').all()
    serializer_class = RemissionSerializer
    permission_classes = [permissions.AllowAny]

    @action( detail = True, methods = [ 'post' ] )
    def close(self, request, pk = None ):
        remission = self.get_object()
        if remission.status == Remission.Status.CLOSED:
            return Response(
                {"error": "La remission ya está cerrada."},
                status=status.HTTP_400_BAD_REQUEST
        )
        with transaction.atomic():
            if not remission.sales.exists():
                return Response(
                    {"error": "No se puede cerrar una remission sin ventas."},
                    status=status.HTTP_400_BAD_REQUEST
            )
            total_sales = remission.sales.aggregate(
            total=Sum(F('subtotal') + F('tax')))['total'] or 0
            total_credits = remission.credits.aggregate(
            total=Sum('amount'))['total'] or 0
            if total_credits > total_sales:
                return Response(
                    {"error": "Los créditos exceden el total vendido."},
                    status=status.HTTP_400_BAD_REQUEST
                    )
            remission.status = Remission.Status.CLOSED
            remission.save()
            return Response({"message": "Remission cerrada correctamente."})
        
    @action( detail = True, methods = [ 'get' ] )
    def summary(self, request, pk = None):
        remission = self.get_object()
        total_sales = remission.sales.aggregate(total=Sum(F('subtotal') + F('tax')))['total'] or 0
        total_credits = remission.credits.aggregate(total=Sum('amount'))['total'] or 0
        sales_count = remission.sales.count()
        balance = total_sales - total_credits
        return Response({
            "total_sales": total_sales,
            "total_credits": total_credits,
            "sales_count": sales_count,
            "balance": balance
        })


class SaleViewSet( viewsets.ModelViewSet ):
    queryset = Sale.objects.select_related('remission').all()
    serializer_class = SaleSerializer
    permission_classes = [permissions.AllowAny]

   

class CreditAssignmentViewSet( viewsets.ModelViewSet ):
    queryset = CreditAssignment.objects.select_related('remission').all()
    serializer_class = CreditAssignmentSerializer
    permission_classes = [permissions.AllowAny]

class ReportViewSet( viewsets.ViewSet ):
    permission_classes = [permissions.AllowAny]
    
    @action(detail=False, methods=['get'])
    def daily_sales(self, request):
        
        
        from_date = request.query_params.get('from')
        to_date = request.query_params.get('to')

        if not from_date or not to_date:
            return Response(
                {"error": "Parameters 'from' and 'to' are required (YYYY-MM-DD format)"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            from_date_obj = parse_date(from_date)
            to_date_obj = parse_date(to_date)

            if not from_date_obj or not to_date_obj:
                raise ValueError()
        except:
            return Response(
                {"error": "Invalid date format. Use YYYY-MM-DD"},
                status=status.HTTP_400_BAD_REQUEST
            )

        from_datetime = timezone.make_aware(datetime.combine(from_date_obj, time.min))
        to_datetime = timezone.make_aware(datetime.combine(to_date_obj, time.max))
        
        sales = Sale.objects.filter(
            created_at__gte=from_datetime,
            created_at__lte=to_datetime
        )

        daily_report = (
            sales
            .annotate(date=TruncDate('created_at'))
            .values('date')
            .annotate(
                total_sales=Sum('subtotal'),
                total_tax=Sum('tax'),
                sales_count=Count('id')
            )
            .order_by('date')
        )

        return Response(list(daily_report))