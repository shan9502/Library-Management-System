from django.shortcuts import render,redirect
from manager.models import Books, Members, BooksReservations, Settings
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from datetime import datetime, timedelta
import pytz
utc=pytz.UTC
# Member Home page view
@csrf_exempt
def HomeView(request):
    if 'Memberlogin' in request.session:
        if request.session['Memberlogin'] == True:
            MId = request.session['MemberId']
            member = Members.objects.get(id = MId)
            books = Books.objects.all().order_by('id').reverse()
            bookreservatons = BooksReservations.objects.all()
            m_days= Settings.objects.filter().order_by('id').latest('id')
            context = {
                    'books': books, 'member': member, 'reserve': bookreservatons
                }
            
            #Ajax getting book id to display the book reservation date
            if 'id' in request.GET:
                bookId = json.loads(request.GET.get('id'))
                print('Book Id:',bookId)
                book_status =Books.objects.get(id = bookId)
                bookD = BooksReservations.objects.filter(book_id = bookId, status = 'Pending')
                if bookD:
                    bookD = BooksReservations.objects.filter(book_id = bookId).order_by('booking_date').latest('id')
                    bookDate = bookD.booking_date + timedelta(days=m_days.max_checkout_days)
                    bookDate = bookDate.strftime('%d/%m/%Y, %H:%M:%S')
                elif book_status.current_status == 'BOOKED':
                    bookDate = "Please check with manager"
                else:
                    bookDate = datetime.now().strftime('%d/%m/%Y, %H:%M:%S')
                    bookDate = "Now"
                    print(bookDate)
                return JsonResponse({"date": bookDate})
            
            # For book search option
            if request.method == 'POST':
                if request.POST.get('search'):
                    search = request.POST.get('search')
                    books = Books.objects.filter(title__icontains = search)
                    if books:
                        context = {
                            'books': books, 'member': member, 'reserve': bookreservatons
                        }
                    else:
                        books = Books.objects.filter(author__icontains = search)
                        context = {
                            'books': books, 'member': member, 'reserve': bookreservatons
                        }
                    return render(request,'member/home.html', context)
                
                #for the booking/Reservaton from member
                elif request.POST.get('resdate'):
                    bookId = request.POST.get('pk')
                    res_date = request.POST.get('resdate')
                    reserve_check2 = BooksReservations.objects.filter(book_id=bookId, status = 'Pending')
                    mcoutday =  m_days.max_checkout_days
                    
                    # conditoin to check if date is valid (won't allow to select past dates)
                    if datetime.strptime(res_date, '%Y-%m-%dT%H:%M') < datetime.now():
                        context = {
                                    'books': books, 'member': member, 'reserve': bookreservatons
                                    ,'message':"Please select a valid date for reservation!"
                                }
                    else:
                        #data to check if user is already have a booking
                        reserve_check = BooksReservations.objects.filter(book_id=bookId, member_id=MId, status = 'Pending')
                    
                        #condition to check if user is already have a booking
                        if reserve_check:
                            context = {
                                'books': books, 'member': member, 'reserve': bookreservatons
                                ,'message':"You already have a reservation on this book! kindly check your reservations."
                            }
                        elif ResrvationOverLapCheck(res_date, reserve_check2, mcoutday) == True:
                            context = {
                                    'books': books, 'member': member, 'reserve': bookreservatons
                                    ,'message':"Reservation is full! Please select an other date."
                                }
                        else:
                            booksreservations = BooksReservations(book_id = bookId, member_id = MId, booking_date = res_date)
                            booksreservations.save()
                            context = {
                                    'books': books, 'member': member, 'reserve': bookreservatons
                                    ,'message':"Your reservarion request has been sent successfully."
                                }
                    return render(request, 'member/home.html', context)

                else:
                    return render(request,'member/home.html', context)
            else:
                return render(request, 'member/home.html', context)
        else:
            return redirect('/user/MemberLogin/')
    else:
        return redirect('/user/MemberLogin/')
    
#check if user selected date is valid or overlaping with other reservations
def ResrvationOverLapCheck(res_date, reserve_check2, mcoutday):
    res_date=datetime.strptime(res_date, '%Y-%m-%dT%H:%M').replace(tzinfo=utc)
    endres_date = res_date + timedelta(days=mcoutday)
    for reservation in reserve_check2:

        endreserve_check2 = reservation.booking_date + timedelta(days=mcoutday)
        endreserve_check2 = endreserve_check2.replace(tzinfo=utc)  
        startreserve_check2 = reservation.booking_date.replace(tzinfo=utc)

        if startreserve_check2 <= res_date <= endreserve_check2:
            return True
        elif startreserve_check2 <= endres_date <=endreserve_check2:
            return True
        else:
            False

def MemberLogoutView(request):
    if request.session['Memberlogin'] == True:
        request.session['Memberlogin'] = False
        request.session['MemberId'] = None
        return redirect('/user/MemberLogin/')
    else:
        return redirect('/user/MemberLogin/')
    
# User Book Reservation details page
def ReservationsView(request):
    if request.session['Memberlogin'] == True:
        if request.method == 'POST':
            if 'pk' in request.POST:
                reserveId = request.POST['pk']
                reservations = BooksReservations.objects.filter(id = reserveId)
                reservations.delete()
                #reservations.save()
        MId = request.session['MemberId']
        member = Members.objects.get(id = MId)
        reservations = BooksReservations.objects.filter(member = MId, status = 'Pending')
        context = {'reservations':reservations, 'member':member}
        return render(request, 'member/reservations.html',context)
    return redirect('/user/MemberLogin/')
# User Book Issued by admin - details page
def BookIssuesView(request):
    if request.session['Memberlogin'] == True:
        MId = request.session['MemberId']
        member = Members.objects.get(id = MId)
        m_outdays = Settings.objects.filter().latest('id')
        reservations = BooksReservations.objects.filter(member = MId, status = 'Confirmed')
        enddates = []
        for reservation in reservations:
            date = reservation.booking_date + timedelta(days=m_outdays.max_checkout_days)
            enddates.append(date)
        context = {'reservations':reservations, 'member':member, 'enddates':enddates}
        return render(request, 'member/issuedbooks.html',context)
    return redirect('/user/MemberLogin/')