from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
	ROLE_CHOICES = [('farmer', 'Farmer'), ('consumer', 'Consumer')]
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='consumer')
	phone = models.CharField(max_length=20, blank=True)
	location = models.CharField(max_length=120, blank=True)
	bio = models.TextField(blank=True)

	def __str__(self):
		return f'{self.user.username} ({self.role})'
