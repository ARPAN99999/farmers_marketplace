from django.urls import path
from . import views

app_name = 'products'
urlpatterns = [
    path('', views.product_list, name='list'),
    path('new/', views.add_product, name='add'),
    path('<int:product_id>/add-to-cart/', views.add_to_cart, name='add_to_cart'),
]
