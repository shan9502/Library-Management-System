from django.db import models

# Create your models here.
class Members(models.Model):
    membership_no = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    mobile = models.CharField(max_length=25)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'members'
    
class Books(models.Model):
    id = models.PositiveIntegerField(primary_key=True, auto_created=True)
    title = models.CharField(max_length=250)
    author = models.CharField(max_length=100)
    language = models.CharField(max_length=100)
    image = models.ImageField(upload_to="media/books/")
    current_status = models.CharField(max_length=6 , default='FREE')
    created_at = models.DateTimeField(auto_created=True, auto_now=True,blank=True)
    updated_at = models.DateTimeField(auto_created=False, auto_now=True ,blank=True)

    class Meta:
        managed = False
        db_table = 'books'