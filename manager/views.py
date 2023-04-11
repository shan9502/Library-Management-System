from django.shortcuts import render, redirect
from .models import Members, Books, Settings, BooksReservations
from users.models import Admin
from django.views.decorators.csrf import csrf_exempt
from .forms import AddBookForm, SettingsForm
from django.shortcuts import get_object_or_404
import datetime
import json
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import os

# Admin Manage Members View 
@csrf_exempt
def ManageMemberView(request):
    if request.session['Adminlogin'] == True:
        settings = Settings.objects.filter().latest('id')
        id = request.session['AdminId']
        #print("Admin ID:",id)
        admin = Admin.objects.filter(id=id).first()
        #getting members from database model
        members = Members.objects.all().order_by('id').reverse()
        context = {'members':members, 'settings':settings, 'admin':admin}
        if request.method == 'POST':
            if request.POST.get('search'):
                search = request.POST.get('search')
                members = Members.objects.filter(name = search)
                context = {'members':members, 'settings':settings, 'admin':admin}
            elif request.POST.get('status'):
                status = request.POST.get('status')
                if status == '1':
                    members = Members.objects.filter(status = 1)
                elif status == '0':
                    members = Members.objects.filter(status = 0)
                context = {'members':members, 'settings':settings, 'admin':admin}
            else:              
                #getting members from database model
                members = Members.objects.all().order_by('id').reverse()
                context = {'members':members, 'settings':settings, 'admin':admin}
        return render(request,'manager/members.html', context)
    else:
        return redirect('/user/AdminLogin')     

# Admin Dashboard View
@csrf_exempt
def DashboardView(request):
    if request.session['Adminlogin'] == True:
        Aid = request.session['AdminId']
        books = Books.objects.all()
        issued = Books.objects.filter(current_status ='BOOKED')
        members = Members.objects.all()
        res_pendings = BooksReservations.objects.filter(status='Pending')
        settings = Settings.objects.filter().latest('id')
        admin = Admin.objects.filter(id=Aid).first()
        transactions = BooksReservations.objects.filter().order_by('id').reverse()[0:8]
        # check books on due function call
        dues_today = checkDuesView()
        # dueCount = checkDuesView()
        context = {'res_pendings':res_pendings,'admin':admin, 
                'settings':settings, 'books':books, 'issued':issued, 
                'members':members, 'transactions':transactions,'dues':dues_today}
        if 'id' in request.POST:
            Tid = json.loads(request.POST['id'])
            value = json.loads(request.POST['value'])
            transaction = BooksReservations.objects.get(id = Tid)
            book = Books.objects.get(id = transaction.book_id)
            #print(type(value),value)
            
            if value == 1 and book.current_status == 'FREE':
                transaction.status ='Confirmed'
                book.current_status = 'BOOKED'
                transaction.save()
                book.save() 
            elif value == 0:
                transaction.status ='Returned'
                book.current_status = 'FREE'
                transaction.save()
                book.save() 
            elif value == 2:
                transaction.status ='Pending'
                book.current_status = 'FREE'
                transaction.save()
                book.save() 
            else:
                print('exception here ----------')
                #transaction.status ='Pending'
                #book.current_status = 'FREE'
                context = {'res_pendings':res_pendings,'admin':admin, 
                'settings':settings, 'books':books, 'issued':issued, 
                'members':members, 'transactions':transactions, 'message':'This Book is Not FREE!'}
                #return render(request,'manager/dashboard.html', context)
            return render(request,'manager/dashboard.html', context)
        return render(request,'manager/dashboard.html', context)
    else:
        return redirect('../user/AdminLogin')

# check books on due function
def checkDuesView():
    counter = 0
    m_outdays =Settings.objects.filter().latest('id').max_checkout_days
    today = datetime.date.today()
    bookingdates = BooksReservations.objects.filter(status = 'Confirmed')
    for book in bookingdates:
        if book.booking_date.date()+ datetime.timedelta(days=m_outdays) == today:
            counter = counter + 1
    return counter

#Confirm/Pending reservations
#@csrf_exempt
# def ManageReservationsView(request):
#     if request.method == 'POST':
#         transId = request.POST.get('tid')
#         value = request.POST.get('value')
#         reservarions = BooksReservations.objects.filter(id = transId)
#         books = Books.objects.get(id=reservarions.book_id)
#         if value == 0:
#             reservarions.status = 'Confirmed'
#             books.current_status = 'BOOKED'
#             reservarions.save()
#         else:
#             reservarions.status = 'Pending'
#             books.current_status = 'FREE'
#             reservarions.save()
#         return redirect('/manager/dashboard/')

#Transactions View and manage
@csrf_exempt
def TransactionsView(request):
    if request.session['Adminlogin'] == True:
        Aid = request.session['AdminId']
        admin = Admin.objects.filter(id=Aid).first()
        transactions = BooksReservations.objects.all()
        
        context = {'admin':admin,
                'transactions':transactions}
        
        if 'search' in request.POST:
            search = request.POST['search']
            status = request.POST['status']
            if search == "":
                # search by status
                if 'status' in request.POST:
                    status = request.POST['status']
                    if status == '/Status':
                        return redirect('/manager/transactions/')
                    transactions = BooksReservations.objects.filter(status = status)
                    context = {'admin':admin,
                        'transactions':transactions}
                    return render(request, 'manager/transactions.html', context)
            elif status == 'Pending' or status == 'Confirmed' or status == 'Returned':
                membername = BooksReservations.objects.filter(member__name = search, status =status)
                book = BooksReservations.objects.filter(book__title = search, status =status)
                author = BooksReservations.objects.filter(book__author = search, status =status)
                if membername:
                    transactions = membername
                    context = {'admin':admin,
                    'transactions':transactions}
                elif book:
                    transactions = book
                    context = {'admin':admin,
                    'transactions':transactions}
                elif author:
                    transactions = author
                    context = {'admin':admin,
                    'transactions':transactions}
                return render(request, 'manager/transactions.html', context)
            # Transactions search view
            else:
                search = request.POST['search']
                membername = BooksReservations.objects.filter(member__name = search)
                book = BooksReservations.objects.filter(book__title = search)
                author = BooksReservations.objects.filter(book__author = search)
                if membername:
                    transactions = membername
                    context = {'admin':admin,
                    'transactions':transactions}
                elif book:
                    transactions = book
                    context = {'admin':admin,
                    'transactions':transactions}
                elif author:
                    transactions = author
                    context = {'admin':admin,
                    'transactions':transactions}
            return render(request,'manager/transactions.html', context)
            
        # change reservation status
        elif 'id' in request.POST:
            Tid = json.loads(request.POST['id'])
            value = json.loads(request.POST['value'])
            transaction = BooksReservations.objects.get(id = Tid)
            book = Books.objects.get(id = transaction.book_id)
            #print(type(value),value)
            
            if value == 1 and book.current_status == 'FREE':
                transaction.status ='Confirmed'
                book.current_status = 'BOOKED'
                # transaction.save()
                # book.save() 
            elif value == 0:
                transaction.status ='Returned'
                book.current_status = 'FREE'
                # transaction.save()
                # book.save() 
            elif value == 2:
                transaction.status ='Pending'
                book.current_status = 'FREE'
                # transaction.save()
                # book.save() 
            else:
                print('exception here ----------')
                #transaction.status ='Pending'
                #book.current_status = 'FREE'
                context = {'admin':admin, 
                'transactions':transactions, 'message':'This Book is Not FREE!'}
                return render(request,'manager/transactions.html', context)
            transaction.save()
            book.save() 
            return render(request,'manager/transactions.html', context)
        else:
            return render(request, 'manager/transactions.html', context)
    else:
        return redirect(request, '/manager/AdminLogin')

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
            os.remove(str(book.image))
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
            status = request.POST.get('status')

            book = Books.objects.get(id=pk)
            if book:
                book.title = title
                book.author = author
                book.language = lang
                book.current_status = status
                if image:
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
#admin profile page
@csrf_exempt
def ProfileView(request):
    if request.session['Adminlogin'] == True:
        admin = Admin.objects.get(id=request.session['AdminId'])
        settings = Settings.objects.filter().latest('id')

        context = {'settings':settings,'admin':admin}
        return render(request, 'manager/profile.html', context)
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
                        to_email = [member.email]
                        library = Settings.objects.filter().latest('id')
                        subject = 'Account Activated'
                        context = {'member': member, 'settings': library}
                        html_msg = render_to_string('manager/activation_email.html',context)
                        plain_msg = strip_tags(html_msg)
                        send_mail(subject, plain_msg,
                               settings.EMAIL_HOST_USER, to_email, html_message=html_msg,fail_silently=True)
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
    
