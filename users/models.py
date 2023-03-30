from django.db import models

# Create your models here.
class Admin(models.Model):
    name = models.CharField(max_length=250)
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True,auto_now=False, blank=True)
    updated_at = models.DateTimeField(auto_now_add=False,auto_now=False, blank=True)

    class Meta:
        managed = False
        db_table = 'admin'

class Members(models.Model):
    membership_no = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=200)
    mobile = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add=True,auto_now=False, blank=True)
    updated_at = models.DateTimeField(auto_now_add=False,auto_now=False, blank=True)
    status = models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'members'