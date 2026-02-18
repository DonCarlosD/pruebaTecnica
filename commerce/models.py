from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

# Create your models here.
class Customer( models.Model ):
    name = models.CharField( max_length = 150 )
    email = models.EmailField( blank = True, null = True )
    is_active = models.BooleanField( default = True )

    def __str__( self ):
        return self.name

class Order( models.Model ):
    customer = models.ForeignKey( Customer, on_delete = models.PROTECT, related_name = 'orders' )
    folio = models.CharField( max_length= 50, unique= True )
    created_at = models.DateTimeField( auto_now_add= True )

    def __str__( self ):
        return self.folio
    
class Remission( models.Model ):

    class Status(models.TextChoices):
        OPEN = "open", "Open"
        CLOSED = "closed", "Closed"

    order = models.ForeignKey( Order, on_delete= models.PROTECT, related_name= 'remissions' )
    folio = models.CharField( max_length = 50, unique= True )
    status = models.CharField( max_length=10, choices=Status.choices, default=Status.OPEN )
    created_at = models.DateTimeField( auto_now_add= True )

    def __str__( self ):
        return self.folio

class Sale( models.Model ):
    remission = models.ForeignKey( Remission, on_delete = models.PROTECT, related_name = 'sales' )
    subtotal = models.DecimalField( max_digits = 12, decimal_places = 2, validators = [ MinValueValidator( Decimal( "0.00" ) ) ] )
    tax = models.DecimalField( max_digits = 12, decimal_places = 2, validators = [ MinValueValidator( Decimal( "0.00" ) ) ] )
    created_at = models.DateTimeField( auto_now_add= True )

    def __str__(self):
        return f"Sale {self.id}"
    
class CreditAssignment( models.Model ):
    remission = models.ForeignKey( Remission, on_delete = models.PROTECT, related_name = 'credits' )
    amount = models.DecimalField( max_digits = 12, decimal_places = 2, validators = [ MinValueValidator( Decimal( "0.01" ) ) ] )
    reason = models.CharField( max_length = 255 )
    created_at = models.DateTimeField( auto_now_add= True )

    def __str__(self):
        return f"Credit {self.id}"