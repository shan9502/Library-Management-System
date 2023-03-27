from django.db import models

# Create your models here.
class UserRegister(models.Model):
    id = models.IntegerField(primary_key=True)
    email = models.CharField(unique=True, max_length=30)
    library_name = models.CharField(max_length=200, blank=True, null=True)
    address = models.CharField(max_length=600)
    phone = models.CharField(max_length=30)
    membership_id = models.IntegerField(unique=True)
    password = models.CharField(max_length=200)
    type = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'users'


class User(models.Model):
    id = models.IntegerField(primary_key=True)
    membership_id = models.IntegerField(unique=True)
    password = models.CharField(max_length=200)
    
    class Meta:
        managed = False
        db_table = 'users'