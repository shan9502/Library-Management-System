from django.shortcuts import render, redirect
from .models import Members, Books
from users.models import Admin
from django.views.decorators.csrf import csrf_exempt

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

def BooksView(request):
    if request.session['Adminlogin'] == True:
        id = request.session['AdminId']
        #print("Admin ID:",id)
        admin = Admin.objects.filter(id=id).first()
        books = Books.objects.all()
        context = {'books':books, 'admin':admin}    
        return render(request,'manager/books.html',context)
    else:
        return redirect('../user/AdminLogin')

# Admin Logout
def AdminLogout(request):
    if request.session['Adminlogin'] == True:
        request.session['Adminlogin'] = False
        request.session['AdminId'] = None
        return redirect('../user/AdminLogin')
    else:
        return redirect('../user/AdminLogin')
    
def AddBook(request):
    if request.session['Adminlogin'] == True:
        id = request.session['AdminId']
        #print("Admin ID:",id)
        admin = Admin.objects.filter(id=id).first()
        if request.method == 'POST':
            title = request.POST.get('title')
            author = request.POST.get('author')
            isbn = request.POST.get('isbn')
            price = request.POST.get('price')
            description = request.POST.get('description')
            image = request.FILES.get('image')
            book = Books(title=title, author=author, isbn=isbn, price=price, description=description, image=image, admin=admin)
            book.save()
            return redirect('../manager/Books')
        else:
            return render(request,'manager/addbooks.html')