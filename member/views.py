from django.shortcuts import render,redirect
from manager.models import Books, Members, BooksReservations
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime

# Member Home page view
@csrf_exempt
def HomeView(request):
    if request.session['Memberlogin'] == True:
        MId = request.session['MemberId']
        member = Members.objects.get(id = MId)
        books = Books.objects.all().order_by('id').reverse()
        reserve = BooksReservations.objects.all()
        context = {
                'books': books, 'member': member, 'reserve': reserve
            }
        #Ajax getting book id to display the book reservation date
        if 'id' in request.GET:
            bookId = json.loads(request.GET.get('id'))
            print('Book Id:',bookId)
            bookD = BooksReservations.objects.filter(id = bookId)
            if bookD:
                bookDate = bookD.booking_date
            else:
                bookDate = datetime.now()
                print(bookDate)
            context = {
                        'books': books, 'member': member, 'reserve': reserve,
                        'bookDate': bookDate
                    }
            return render(request,'member/home.html', context)
        # For the search option
        if request.method == 'POST':
            if request.POST.get('search'):
                search = request.POST.get('search')
                books = Books.objects.filter(title__icontains = search)
                if books:
                    context = {
                        'books': books, 'member': member, 'reserve': reserve
                    }
                else:
                    books = Books.objects.filter(author__icontains = search)
                    context = {
                        'books': books, 'member': member, 'reserve': reserve
                    }
                return render(request,'member/home.html', context)
            #for the booking/Reservaton
            elif request.POST.get(''):
                pass
            else:
                return render(request,'member/home.html', context)
        else:
            return render(request, 'member/home.html', context)
    else:
        return redirect('/user/MemberLogin/')
    
def MemberLogoutView(request):
    if request.session['Memberlogin'] == True:
        request.session['Memberlogin'] = False
        request.session['MemberId'] = None
        return redirect('/user/MemberLogin/')
    else:
        return redirect('/user/MemberLogin/')
    