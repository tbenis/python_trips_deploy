from django.shortcuts import render, redirect
from .models import User, Trip, All_Trip
from django.contrib import messages
import datetime
# Create your views here.
def index(request):
    # User.objects.all().delete()
    # Trip.objects.all().delete()
    # All_Trip.objects.all().delete()
    return render(request, 'travelApp/login_and_reg.html')
def rvalidate(request):
    if request.method == 'POST':
        postData = {
            'name': request.POST['name'],
            'uname': request.POST['uname'],
            'pw': request.POST['pw'],
            'cpw': request.POST['cpw'],
        }
        results = User.objects.rvalidate(postData)
        try:
            if results[0]:
                for error in results[1]:
                    messages.error(request, error)
                return redirect('/')
            else:
                request.session['logged_in_user'] = results[1].id
                return redirect('/success')
        except:
            print "ERROR"
def lvalidate(request):
    if request.method == 'POST':
        postData = {
            'uname': request.POST['uname'],
            'pw': request.POST['pw']
        }
        results = User.objects.lvalidate(postData)
        try:
            if not results[0]:
                messages.error(request, results[1])
                return redirect('/')
            else:
                request.session['logged_in_user'] = results[1].id
                return redirect('/success')
        except:
            messages.error(request, results[1])
            return redirect('/')
def success(request):
    curr_user =  User.objects.get(id = request.session['logged_in_user'])
    curr_user_trips = All_Trip.objects.filter(user_id = curr_user)
    alltrips = Trip.objects.all().exclude(user_id = curr_user)
    for x in curr_user_trips:
        alltrips = alltrips.exclude(id = x.trip.id)
    context = {
        'user' : User.objects.get(id = request.session['logged_in_user']),
        'curr_user_trips' : curr_user_trips,
        'alltrips' : alltrips
    }
    # print "*"*50
    # print alltrips
    return render(request, 'travelApp/dashboard.html', context)
# User.objects.get(id = request.session['logged_in_user']

def travels(request):

    datenow = datetime.datetime.now()
    datefrom = datetime.datetime.strptime(str(request.POST['datefrom']), '%Y-%m-%d')
    dateto = datetime.datetime.strptime(request.POST['dateto'], '%Y-%m-%d')
    print "*"*20
    print 'datenow : ' , datenow
    print "*"*20
    print 'datefrom : ' , datefrom
    print "*"*20
    print 'dateto : ' , dateto

    postData ={

        'destination' : request.POST['destination'],
        'description' : request.POST['description'],
        'datefrom' : datefrom,
        'dateto' : dateto,
        'datenow' : datenow,
        'user' : User.objects.get(id = request.session['logged_in_user'])
    }
    results = Trip.objects.trip_maker(postData)
    if results[0]:

        for error in results[1]:
            print error
            messages.error(request, error)
        return redirect('/add')
    else:
        curr_user =  User.objects.get(id = request.session['logged_in_user'])
        alltrips = All_Trip.objects.filter(user = curr_user)
        All_Trip.objects.create(user= curr_user, trip = results[1])
        return redirect('/success')

    return redirect("/add")

def destination(request, id):
    trip_info = Trip.objects.get(id = id)
    # curr_user =  User.objects.get(id = request.session['logged_in_user'])
    other_users = All_Trip.objects.filter(trip_id = id)
    context ={
    'trip_info' :trip_info,
    'other_users' :  other_users
    }
    print "6"*25
    print "6"*2
    return render(request, 'travelApp/destination.html', context)
def add(request):
    return render(request, 'travelApp/add_plan.html')
def join(request, id):
    curr_user =  User.objects.get(id = request.session['logged_in_user'])
    new_trip = Trip.objects.get(id=id)
    All_Trip.objects.create(user=curr_user, trip= new_trip)
    return redirect('/success')
def delete(request, id):
    Trip.objects.get(id=id).delete()
    return redirect('/success')
def logout(request):
    request.session.clear()
    request.session.pop('logged_in_user', None)
    return redirect('/')
