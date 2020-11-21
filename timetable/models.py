from djongo import models

# Create your models here

class Timetable(models.Model):
    user = models.CharField(max_length=30)
    day = models.CharField(max_length=10)
    time = models.TimeField(auto_now=False)
    prof = models.CharField(max_length=30)

