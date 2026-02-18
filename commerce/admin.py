from django.contrib import admin
from .models import Customer, Order, Remission, Sale, CreditAssignment
# Register your models here.
admin.site.register( Customer )
admin.site.register( Order )
admin.site.register( Remission )
admin.site.register( Sale )
admin.site.register( CreditAssignment )