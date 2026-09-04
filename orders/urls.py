from django.urls import path
from . import views

app_name = 'orders'
urlpatterns = [
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('confirmation/<int:order_id>/', views.confirmation, name='confirmation'),
    path('mine/', views.my_orders, name='my_orders'),
    path('farmer/', views.farmer_orders, name='farmer_orders'),
]
