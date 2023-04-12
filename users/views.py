from django.shortcuts import render, redirect
from .models import Admin, Members
from .forms import Adminform, MemberForm, LoginForm
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password



# Admin Registration form view.
@csrf_exempt
def AdminRegView(request):
    if request.method == 'POST':
        form = Adminform(request.POST)        
        if form.is_valid():
            #form.save()
            aname = form.cleaned_data['name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            reg = Admin(name = aname, email = email, password = make_password(password))
            reg.save()
            #context = {'form': form}
            return redirect('/user/AdminLogin')
        else:
            #return HttpResponse('<h1>Validatoin Error</h1>')
            context = {'form': form, 'type':'Manager','pagelink':'AdminLogin'}
            return render(request, 'registration.html', context)
    else:
        form = Adminform()
        context = {'form': form, 'type':'Manager','pagelink':'AdminLogin'}
        return render(request, 'registration.html', context)
    
# Member Registration form view
@csrf_exempt
def MemberRegView(request):
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            aname = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            password = form.cleaned_data['password']
            reg = Members(name = aname, email = email, password = make_password(password),mobile = phone)
            reg.save()
            #context = {'form': form}
            return redirect('/user/MemberLogin')
        else:
            #return HttpResponse('<h1>Validatoin Error</h1>')
            context = {'form': form, 'type':'Member','pagelink':'MemberLogin'}
            return render(request, 'registration.html', context)
    else:
        form = MemberForm()
        context = {'form': form, 'type':'Member','pagelink':'MemberLogin'}
        return render(request, 'registration.html', context)

# Admin Login Form
@csrf_exempt
def AdminLoginView(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            admin = Admin.objects.filter(email = email).first()
            if admin:
                if check_password(password, admin.password):
                    #return redirect('home')
                    request.session['Adminlogin']= True
                    request.session['AdminId'] = admin.id
                    #return HttpResponse('<h1>Admin Login Success</h1>')
                    return redirect('/manager/')
                else:
                    #return HttpResponse('<h1>Password Not Matching</h1>')
                    context = {'form': form, 'type':'Member', 'msg':'Incorrect password','pagelink':'AdminReg'}
                    return render(None,'login.html', context)
            else:
                #return HttpResponse('<h1>Email not Matching</h1>')
                context = {'form': form, 'type':'Member', 'msg':'This email is not registered','pagelink':'AdminReg'}
                return render(None,'login.html', context) 
        else:
            context = {'form': form, 'type':'Manager','msg':'Validation Error.'}
            #return render(request,'login.html', context)
            return render(None,'login.html', context) 
    else:
        form = LoginForm()
        context = {'form': form, 'type':'Manager','pagelink':'AdminReg'}
        return render(request, 'login.html', context)

#Member Login Form
@csrf_exempt  
def MemberLoginView(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            #taking the inuputs from form
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            #taking the first row with the matched email
            member = Members.objects.filter(email = email).first()
            if member:
                if check_password(password, member.password):
                    #return redirect('home')
                    if member.status == 0:
                        context = {'form': form, 'type':'Member', 'msg':'Please wait until your accout is activated by library manager.','pagelink':'MemberReg'}
                        return render(None,'login.html', context)
                    else:
                        request.session['Memberlogin']= True
                        request.session['MemberId'] = member.id
                        #return HttpResponse('<h1>Member Login Success</h1>')
                        return redirect('/')
                else:
                    #return HttpResponse('<h1>Password Not Matching</h1>')
                    context = {'form': form, 'type':'Member', 'msg':'Incorrect password','pagelink':'MemberReg'}
                    return render(None,'login.html', context)                   
            else:
                #return HttpResponse('<h1>Email not Matching</h1>')
                context = {'form': form, 'type':'Member', 'msg':'This email is not registered','pagelink':'MemberReg'}
                return render(None,'login.html', context)
        else:
            context = {'form': form, 'type':'Member','msg':'Validation Error.'}
            #return render(request,'login.html', context)
            return render(None,'login.html', context) 
    else:
        form = LoginForm()
        context = {'form': form, 'type':'Member','pagelink':'MemberReg'}
        return render(request, 'login.html', context)