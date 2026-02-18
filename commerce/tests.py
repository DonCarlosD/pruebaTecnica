from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal
from .models import Customer, Order, Remission, Sale, CreditAssignment


class RemissionCloseTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.customer = Customer.objects.create(name="Test Customer", email="test@test.com")
        self.order = Order.objects.create(customer=self.customer, folio="FOL-001")
        self.remission = Remission.objects.create(order=self.order, folio="REM-001")

    def test_close_fails_without_sales(self):
        """Test que el cierre falla si la remisión no tiene ventas"""
        response = self.client.post(f'/commerce/api/v1/remissions/{self.remission.id}/close/')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("No se puede cerrar una remission sin ventas", response.data['error'])
        
        self.remission.refresh_from_db()
        self.assertEqual(self.remission.status, Remission.Status.OPEN)

    def test_close_fails_if_credits_exceed_sales(self):
        """Test que el cierre falla si créditos > ventas"""
        Sale.objects.create(
            remission=self.remission,
            subtotal=Decimal("100.00"),
            tax=Decimal("10.00")
        )
        
        CreditAssignment.objects.create(
            remission=self.remission,
            amount=Decimal("200.00"),
            reason="Excess credit"
        )
        
        response = self.client.post(f'/commerce/api/v1/remissions/{self.remission.id}/close/')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Los créditos exceden el total vendido", response.data['error'])
        
        self.remission.refresh_from_db()
        self.assertEqual(self.remission.status, Remission.Status.OPEN)

    def test_close_succeeds_with_valid_conditions(self):
        """Test que el cierre funciona cuando se cumplen las condiciones"""
        Sale.objects.create(
            remission=self.remission,
            subtotal=Decimal("100.00"),
            tax=Decimal("10.00")
        )
        
        CreditAssignment.objects.create(
            remission=self.remission,
            amount=Decimal("50.00"),
            reason="Valid credit"
        )
        
        response = self.client.post(f'/commerce/api/v1/remissions/{self.remission.id}/close/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Remission cerrada correctamente", response.data['message'])
        
        self.remission.refresh_from_db()
        self.assertEqual(self.remission.status, Remission.Status.CLOSED)


class DailySalesReportTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.customer = Customer.objects.create(
            name="Test Customer",
            email="test@test.com"
        )
        self.order = Order.objects.create(
            customer=self.customer,
            folio="FOL-002"
        )
        self.remission = Remission.objects.create(
            order=self.order,
            folio="REM-002"
        )

    def test_daily_sales_report_groups_correctly_two_days(self):
        """Test que el reporte diario agrupa correctamente (mínimo dos días distintos)"""

        now = timezone.now()
        today = now.date()
        yesterday = today - timedelta(days=1)

        sale_yesterday = Sale.objects.create(
            remission=self.remission,
            subtotal=Decimal("200.00"),
            tax=Decimal("20.00")
        )

        Sale.objects.filter(id=sale_yesterday.id).update(
            created_at=timezone.make_aware(
                datetime.combine(yesterday, datetime.min.time()).replace(hour=12)
            )
        )

        Sale.objects.create(
            remission=self.remission,
            subtotal=Decimal("100.00"),
            tax=Decimal("10.00"),
            created_at=now
        )

        Sale.objects.create(
            remission=self.remission,
            subtotal=Decimal("50.00"),
            tax=Decimal("5.00"),
            created_at=now
        )

        response = self.client.get(
            f'/commerce/api/v1/reports/daily_sales/?from={yesterday.strftime("%Y-%m-%d")}&to={today.strftime("%Y-%m-%d")}'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data

        self.assertEqual(len(data), 2)

        self.assertEqual(data[0]['sales_count'], 1)
        self.assertEqual(Decimal(str(data[0]['total_sales'])), Decimal("200.00"))
        self.assertEqual(Decimal(str(data[0]['total_tax'])), Decimal("20.00"))

        self.assertEqual(data[1]['sales_count'], 2)
        self.assertEqual(Decimal(str(data[1]['total_sales'])), Decimal("150.00"))
        self.assertEqual(Decimal(str(data[1]['total_tax'])), Decimal("15.00"))