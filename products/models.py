from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
	CATEGORY_CHOICES = [
		('vegetables', 'Vegetables'),
		('fruits', 'Fruits'),
		('grains', 'Grains'),
		('dairy', 'Dairy'),
		('other', 'Other'),
	]
	farmer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
	name = models.CharField(max_length=120)
	description = models.TextField()
	category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
	price = models.DecimalField(max_digits=10, decimal_places=2)
	unit = models.CharField(max_length=30, default='kg')
	stock = models.PositiveIntegerField(default=0)
	is_available = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-created_at']

	def __str__(self):
		return self.name
