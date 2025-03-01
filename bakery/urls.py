from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

#app_name = 'bakery'


router = DefaultRouter()
router.register(r'products', views.ProductViewSet)
router.register(r'sales', views.SaleViewSet)
router.register(r'customers', views.CustomerViewSet)


urlpatterns = [

    # Main views
    path('', views.dashboard_view, name='dashboard'),
    path('pos/', views.pos_view, name='pos'),
    path('reports/daily-sales/', views.daily_sales_report, name='daily_sales_report'),
    path('reports/product-popularity/', views.product_popularity_report, name='product_popularity_report'),
    path('reports/export/', views.export_report, name='export_report'),
    path('create-sale/', views.create_sale, name='create_sale'),
    path('products-management/', views.product_management_view, name='product_management'),
    path('edit-product/', views.edit_product, name='edit_product'),
    path('delete-product/', views.delete_product, name='delete_product'),
    
    # Separate API urls
    path('api/', include((router.urls, 'api'))),
]