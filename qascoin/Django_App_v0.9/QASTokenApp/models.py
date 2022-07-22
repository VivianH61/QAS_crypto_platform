from django.db import models

# Create your models here.
class Registration(models.Model):
	email = models.EmailField()
	is_verified = models.BooleanField(default=False)
	token = models.CharField(max_length=100, default=None)