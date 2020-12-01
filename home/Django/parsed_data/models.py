## parsed_data/models.py
from djongo import models

class Bus_To_Station_From_School(models.Model):
    hour = models.IntegerField(default = 0)
    minite = models.IntegerField(default =0)

class Bus_To_School_From_Station(models.Model):
    hour = models.IntegerField(default = 0)
    minite = models.IntegerField(default =0)

class Bus_To_Station_From_School_Sunday(models.Model):
    hour = models.IntegerField(default = 0)
    minite = models.IntegerField(default =0)

class Bus_To_School_From_Station_Sunday(models.Model):
    hour = models.IntegerField(default = 0)
    minite = models.IntegerField(default =0)

class corona_prevent_notice(models.Model):
    title = models.CharField(max_length = 50)
    link = models.CharField(max_length = 200)
    date = models.DateField()

class corona_action_notice(models.Model):
    title = models.CharField(max_length = 50)
    link = models.CharField(max_length = 200)
    date = models.DateField()
    
class common_notice(models.Model):
    title = models.CharField(max_length = 50)
    link = models.CharField(max_length = 200)
    date = models.DateField()

class event_notice(models.Model):
    title = models.CharField(max_length = 50)
    link = models.CharField(max_length = 200)
    date = models.DateField()

class scholarship_notice(models.Model):
    title = models.CharField(max_length = 50)
    link = models.CharField(max_length = 200)
    date = models.DateField()

class career_notice(models.Model):
    title = models.CharField(max_length = 50)
    link = models.CharField(max_length = 200)
    date = models.DateField()

class weekly_menu(models.Model):
    link = models.CharField(max_length =200)

class club_intro(models.Model):
    category = models.CharField(max_length = 30)
    name = models.CharField(max_length =50)
    explanation = models.CharField(max_length = 3000)

class lecture_rate(models.Model):
    lecture = models.CharField(max_length =30)
    teacher = models.CharField(max_length =10)
    rate = models.FloatField()
    semester = models.CharField(max_length =10)
    context = models.CharField(max_length =1000)
