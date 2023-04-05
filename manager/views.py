from django.shortcuts import render, redirect
from .models import Members, Books, Settings, BooksReservations
from users.models import Admin
from django.views.decorators.csrf import csrf_exempt
from .forms import AddBookForm, SettingsForm
from django.shortcuts import get_object_or_404
from datetime import datetime

# Admin Manage Members View 
@csrf_exempt
def ManageMemberView(request):
    if request.session['Adminlogin'] == True:
        settings = Settings.objects.filter().latest('id')
        id = request.session['AdminId']
        #print("Admin ID:",id)
        admin = Admin.objects.filter(id=id).first()
        if request.method == 'POST':
            if request.POST.get('search'):
                search = request.POST.get('search')
                members = Members.objects.filter(name = search)
                context = {'members':members, 'settings':settings, 'admin':admin}
            else:              
                #getting members from database model
                members = Members.objects.all()
                context = {'members':members, 'settings':settings, 'admin':admin}
        return render(request,'manager/members.html', context)
    else:
        return redirect('/user/AdminLogin')

# Admin Dashboard View
def DashboardView(request):
    if request.session['Adminlogin'] == True:
        id = request.session['AdminId']
        books = Books.objects.all()
        issued = Books.objects.filter(current_status ='BOOKED')
        members = Members.objects.all()
        res_pendings = BooksReservations.objects.filter(status='Pending')
        settings = Settings.objects.filter().latest('id')
        admin = Admin.objects.filter(id=id).first()
        context = {'res_pendings':res_pendings,'admin':admin, 'settings':settings, 'books':books, 'issued':issued, 'members':members}  
        return render(request,'manager/dashboard.html', context)
    else:
        return redirect('../user/AdminLogin')

# Book View and Add Books Form
@csrf_exempt
def BooksView(request):
    if request.session['Adminlogin'] == True:
        id = request.session['AdminId']
        #print("Admin ID:",id)
        settings = Settings.objects.filter().latest('id')
        admin = Admin.objects.filter(id=id).first()
        books = Books.objects.all()
        form = AddBookForm()
        context = {'form': form, 'books':books, 'admin':admin, 'settings':settings} 
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

# delete books
def deleteBookView(request):
    if request.session['Adminlogin'] == True:
        if request.method == 'POST':
            pk = request.POST.get('pk')
            #print("Book Id:",pk)
            book = Books.objects.get(id=pk)
            book.delete()
        return redirect('/manager/books')

# edit books
@csrf_exempt        
def editBookView(request,):
    if request.session['Adminlogin'] == True:
        if request.method == 'POST':
            pk = request.POST.get('pk')
            #print("Book Id:",pk)
            title =request.POST.get('title')
            author = request.POST.get('author')
            lang = request.POST.get('lang')
            image = request.FILES.get('image')

            book = Books.objects.get(id=pk)
            if book:
                book.title = title
                book.author = author
                book.language = lang
                book.image = image
                book.save()
                return redirect('/manager/books')
        else:
            return redirect('/manager/books')


# BooK Search
@csrf_exempt    
def SearchBookView(request):
    if request.session['Adminlogin'] == True:
        if request.method == 'POST':
            search = request.POST.get('search')
            books = Books.objects.filter(title__icontains=search)
            if books:
                context = {'books':books}
            else:
                books = Books.objects.filter(author__icontains=search)
                context = {'books':books}
            return render(request,'manager/books.html',context)
        else:
            return redirect('/manager/books')
    else:
        return redirect('/user/AdminLogin')


# Admin Settings Updation
@csrf_exempt
def SettingsAdminView(request):
    if request.session['Adminlogin'] == True:
        s_id = Settings.objects.filter().latest('id')
        settings = get_object_or_404(Settings, id = s_id.id)
        form = SettingsForm(instance=settings)
        admin = Admin.objects.get(id=request.session['AdminId'])
        if request.method == 'POST':
            form = SettingsForm(request.POST,instance=settings)
            if form.is_valid():
                form.save()
                context = {'settings':s_id,'admin':admin,'form':form,'msg':'Settings Updated Successfully'}
                return render(request,'manager/settings.html', context)       
            else:
                print(form.errors)
                context = {'settings':s_id,'msg': "Form Validation Failed"}
                return redirect('manager/settings/', context)
        else:
            if Settings.objects.all().exists():
                context = {'settings':s_id,'admin':admin,'form':form}
                return render(request,'manager/settings.html', context)
            else:
                context = {'settings':s_id,'admin':admin,'form':form}
                return render(request,'manager/settings.html', context)
    else:
        return redirect('/user/AdminLogin')




# Random Membership Id Generator
def generateMembId():
    import random
    uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    lowercase = uppercase.lower()
    digits = "0123456789"
    symbols = "@#$%&*=+<>? "

    upper, lower, nums, syms = True, True, True, False
    all = ""

    if upper:
        all + uppercase
    if lower:
        all += lowercase
    if nums:
        all += digits
    if syms:
        all += symbols

    length = 10
    amount = 20

    password = "".join(random.sample (all, length))
    return (password)

# Member availability check with new Membership Id (True or False)
def MemberAvailabilityCheck(membership_id):
    if membership_id:
        member = Members.objects.filter(membership_no=membership_id)
        if member:
            return True
        else:
            return False

# Admin Enable Member and assign Membership Id
def EnableMember(request, pk):
    if request.session['Adminlogin'] == True:
        if pk:
            member_on_mid = True
            while member_on_mid == True:
                mid = generateMembId()
                member_on_mid = MemberAvailabilityCheck(mid)
                if member_on_mid == False:
                    member = Members.objects.get(id=pk)
                    if member.membership_no == None:
                        member.membership_no = mid
                    else:
                        pass
                    member.status = 1
                    member.save()
                else:
                    pass
        return redirect('/manager/manageMembers')
    else:
        return redirect('/user/AdminLogin')

# Admin Disable Member
def DisableMember(request, pk):
    if request.session['Adminlogin'] == True:
        if pk:
            member = Members.objects.get(id=pk)
            member.status = 0
            member.save()
        return redirect('/manager/manageMembers')
    else:
        return redirect('/user/AdminLogin')
