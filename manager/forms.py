from .models import Books
from django.forms import ModelForm

class AddBookForm(ModelForm):
    class Meta:
        model = Books
        fields = ['title', 'author', 'language', 'image']
