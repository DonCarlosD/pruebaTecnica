from django.core.management.base import BaseCommand
from decimal import Decimal
from commerce.models import Customer, Order, Remission, Sale, CreditAssignment


class Command(BaseCommand):
    help = "Base de datos con datos de ejemplo para desarrollo y pruebas"

    def handle(self, *args, **kwargs):

        self.stdout.write(self.style.SUCCESS("Cargando datos..."))

        customer = Customer.objects.create(
            name="Carlos Demo",
            email="carlos@demo.com"
        )

        order = Order.objects.create(
            customer=customer,
            folio="FOLIO-DEMO-001"
        )

        remission = Remission.objects.create(
            order=order,
            folio="REM-DEMO-001"
        )

        Sale.objects.create(
            remission=remission,
            subtotal=Decimal("100.00"),
            tax=Decimal("10.00")
        )

        Sale.objects.create(
            remission=remission,
            subtotal=Decimal("50.00"),
            tax=Decimal("5.00")
        )

        CreditAssignment.objects.create(
            remission=remission,
            amount=Decimal("20.00"),
            reason="Credito demo"
        )

        self.stdout.write(self.style.SUCCESS("Seed completado correctamente."))
