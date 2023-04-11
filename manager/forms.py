from .models import Books, Settings
from users.models import Admin
from django.forms import ModelForm

class AddBookForm(ModelForm):
    class Meta:
        model = Books
        fields = ['title', 'author', 'language', 'image']

class SettingsForm(ModelForm):
    class Meta:
        model = Settings
        fields = ['library_name','max_checkout_days','late_fees']

# class ProfileForm(ModelForm):
#     class Meta:
#         model = Admin
#         fields = ['']