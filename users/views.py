from django.shortcuts import render, redirect
from .models import UserRegister
from .models import User
#from django.contrib.auth import authenticate, login


# Create your views here.
class UserForm():
    def UserRegisterView(request):
        if request.method == 'POST':
            form = UserRegister(request.POST)
            if form.is_valid():
                User.objects.get()

                form.save()
                # username = form.cleaned_data.get('username')
                # raw_password = form.cleaned_data.get('password1')
                # user = authenticate(username=username, password=raw_password)
                login(request, user)
                return redirect('home')
        else:
            form = Users()
        return render(request, '/register.html', {'form': form})