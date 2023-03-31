from django.shortcuts import render, redirect
from .models import Members, Books
from users.models import Admin
from django.views.decorators.csrf import csrf_exempt
from .forms import AddBookForm

# Create your views here.

@csrf_exempt
def ManageMemberView(request):
    #getting members from database model
    members = Members.objects.all()
    #setting them to variables
    # name = members.get('name')
    # membership_id = members.get('membership_no')
    # phone = members.get('mobile')
    # join = members.get('created_at')
    # status = members.get('status')

    #context = {'name': name, 'phone':phone, 'membership_id': membership_id, 'join': join,'status': status}
    
    #rendering members.html page
    return render(request,'manager/members.html', {'members':members})
    #return render(request, 'manager/members.html')

def DashboardView(request):
    if request.session['Adminlogin'] == True:
        id = request.session['AdminId']
        #print("Admin ID:",id)
        admin = Admin.objects.filter(id=id).first()
        context = {'admin':admin}  
        return render(request,'manager/dashboard.html', context)
    else:
        return redirect('../user/AdminLogin')

# Book View and Add Books Form
@csrf_exempt
def BooksView(request):
    if request.session['Adminlogin'] == True:
        id = request.session['AdminId']
        #print("Admin ID:",id)
        admin = Admin.objects.filter(id=id).first()
        books = Books.objects.all()
        form = AddBookForm()
        context = {'form': form, 'books':books, 'admin':admin} 
        if request.method == 'POST':
            formCheck = AddBookForm(request.POST, request.FILES)
            if formCheck.is_valid():
                formCheck.save()
                #return redirect('../manager/Books')
                #return render(request,'manager/books.html',context)
        return render(request,'manager/books.html',context)
    else:
        return redirect('/user/AdminLogin')

# Admin Logout
def AdminLogout(request):
    if request.session['Adminlogin'] == True:
        request.session['Adminlogin'] = False
        request.session['AdminId'] = None
        return redirect('/user/AdminLogin')
    else:
        return redirect('/user/AdminLogin')

def deleteBookView(request):
    if request.session['Adminlogin'] == True:
        if request.method == 'POST':
            book = Books.objects.get(id=32)
            context = {'item':book}
            # book = Books.objects.filter(id=pk).first()
            # book.delete()
            return render(request,'manager/books.html',context)
        return render(request,'manager/books.html',context)