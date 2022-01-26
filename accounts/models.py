from django.db import models
import datetime
from django.contrib.auth.models import User

# Create your models here.

# HOST MODEL


class profile_details(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    fstname=models.CharField(max_length=250)
    u_nm=models.CharField(max_length=150)
    urmail=models.EmailField()
    unicode = models.CharField(max_length=100,null=True)
    timestamp = models.DateTimeField(null=True)
    verified = models.BooleanField(default=False)
    
class Host(models.Model):
    id = models.AutoField
    host_name = models.CharField(max_length=50)
    host_email = models.EmailField(blank=True, null=True)
    host_phone = models.IntegerField(max_length=10)
    host_image = models.ImageField(upload_to='img/doctors')
    host_desc = models.CharField(max_length=50)
    address = models.CharField(max_length=100,default="HealthPlus, GT-22, Mumbai")
    status = models.BooleanField(default=True)
    available = models.CharField(max_length=50,default='')
    current_meeting_id = models.IntegerField(blank=True, null=True)
    t09to10=models.BooleanField(default=True)
    t10to11=models.BooleanField(default=True)
    t11to12=models.BooleanField(default=True)
    t13to14=models.BooleanField(default=True)
    t14to15=models.BooleanField(default=True)
    t15to16=models.BooleanField(default=True)
    t16to17=models.BooleanField(default=True)

    def __str__(self):
        return str(self.id) + " : " + str(self.host_name)

# MEETING MODEL
class Meeting(models.Model):
    id = models.AutoField
    visitor_name = models.CharField(max_length=50)
    visitor_email = models.EmailField(blank=True, null=True)
    visitor_phone = models.IntegerField(max_length=10)
    host = models.CharField(max_length=50, default="")
    date = models.DateField(default=datetime.date.today())
    time_in = models.TimeField(default=datetime.time(9,0,0))
    time_out = models.TimeField(default=datetime.time(17,0,0))
    time_slott=models.CharField(max_length=50,default='t09to10')
    checked_out=models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)+ ' : ' + str(self.visitor_name)

