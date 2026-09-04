from django.db import models
from django.contrib.auth.models import User
from products.models import Product


class Order(models.Model):
	STATUS_CHOICES = [('placed', 'Placed'), ('confirmed', 'Confirmed'), ('delivered', 'Delivered')]
	consumer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
	delivery_address = models.TextField()
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='placed')
	total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-created_at']

class OrderItem(models.Model):
	order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
	product = models.ForeignKey(Product, on_delete=models.PROTECT)
	quantity = models.PositiveIntegerField()
	price = models.DecimalField(max_digits=10, decimal_places=2)

	@property
	def line_total(self):
		return self.quantity * self.price
