from djongo import models

# Create your models here

class Plan(models.Model):
    user = models.CharField(max_length=30)
    date = models.DateField(auto_now_add=False, null=False)
    place = models.CharField(max_length=100)
    content = models.CharField(max_length=255)
