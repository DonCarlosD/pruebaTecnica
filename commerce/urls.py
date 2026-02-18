from rest_framework import routers
from django.urls import path, include
from commerce import views

router = routers.DefaultRouter()
router.register( r'customers', views.CustomerViewSet, 'customers' )
router.register( r'orders', views.OrderViewSet, 'orders' )
router.register( r'remissions', views.RemissionViewSet, 'remissions' )
router.register( r'sales', views.SaleViewSet, 'sales' )
router.register( r'credits', views.CreditAssignmentViewSet, 'credits' )
router.register( r'reports', views.ReportViewSet, 'reports' )

urlpatterns = [
    path( 'api/v1/', include( router.urls ) )
]
