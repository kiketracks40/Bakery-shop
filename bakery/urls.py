from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'products', views.ProductViewSet)
router.register(r'sales', views.SaleViewSet)
router.register(r'customers', views.CustomerViewSet)


urlpatterns = [
path('', include(router.urls)),
path('reports/daily-sales/', views.daily_sales_report, name='daily_sales_report'),
path('reports/product-popularity/', views.product_popularity_report, name='product_popularity_report'),
path('reports/export/', views.export_report, name='export_report'),

]