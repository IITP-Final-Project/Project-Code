from djongo import models

# Create your models here

class Plan(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.CharField(max_length=30)
    date = models.DateField(auto_now_add=False, null=False)
    place = models.CharField(max_length=100)
    content = models.CharField(max_length=255)

class Plan2(models.Model):
    user = models.CharField(max_length=30)
    date = models.DateField(auto_now_add=False, null=False)
    place = models.CharField(max_length=100)
    content = models.CharField(max_length=255)

