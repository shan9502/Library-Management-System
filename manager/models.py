from django.db import models


# Create your models here.
class Members(models.Model):
    id = models.PositiveIntegerField(primary_key=True, auto_created=True)
    membership_no = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    mobile = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True ,editable=False)
    status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'members'
    def __str__(self):
        return self.id
    
class Books(models.Model):
    id = models.PositiveIntegerField(primary_key=True, auto_created=True)
    title = models.CharField(max_length=250)
    author = models.CharField(max_length=100)
    language = models.CharField(max_length=100)
    image = models.ImageField(upload_to="static/media/books/")
    current_status = models.CharField(max_length=6 , default='FREE')
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True ,editable=False)

    class Meta:
        managed = False
        db_table = 'books'
    def __str__(self):
        return self.id

class Settings(models.Model):
    id = models.PositiveIntegerField(primary_key=True,auto_created=True, blank=True)
    library_name = models.CharField(max_length=200)
    max_checkout_days = models.PositiveIntegerField(max_length=10)
    late_fees = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        managed = False
        db_table = 'settings'

class BooksReservations(models.Model):
    id = models.PositiveIntegerField(primary_key=True,auto_created=True, blank=True)
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    member = models.ForeignKey(Members, on_delete=models.CASCADE)
    booking_date = models.DateTimeField()
    status = models.CharField(max_length=9, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        managed = False
        db_table = 'books_reservations'