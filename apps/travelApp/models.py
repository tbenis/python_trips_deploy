from __future__ import unicode_literals
import datetime
from django.db import models
from django.conf import settings
import bcrypt

# Create your models here.
class UserManager(models.Manager):
    def rvalidate(self, postData):
        errors = []
        flag = False
        if not postData['name']:
            errors.append('You must enter your name')
            flag = True
        elif len(postData['name']) < 3:
            errors.append('Your Name must be more than 3 characters')
            flag = True
        if not postData['uname']:
            errors.append('Please enter A User Name')
            flag = True
        elif len(postData['uname']) < 3:
            errors.append('Your Username name must be more than 3 characters')
            flag = True
        if not postData['pw']:
            errors.append('Please enter a password')
            flag = True
        elif len(postData['pw']) < 3:
            errors.append('Your password must be more than 3 characters')
            flag = True
        elif not postData['cpw']:
            errors.append('Please enter a confirmation password')
            flag = True
        elif postData['pw'] != postData['cpw']:
            errors.append('Confirmation password and password must match!')
            flag = True
        if flag:
            print errors
            return (flag, errors)
        if not flag:
            hashedPw = bcrypt.hashpw(postData['pw'].encode(), bcrypt.gensalt())
            User.objects.create(name = postData['name'], uname = postData['uname'], password= hashedPw)
            user = User.objects.last()
            return (flag, user)

    def lvalidate(self, postData):
        try:
            user = User.objects.get(uname = postData['uname'])
            password =  postData['pw'].encode()
            hashed = user.password.encode()

            if bcrypt.hashpw(password, hashed) == hashed:
                return (True, user)
            else:
                return (False, "Login credentials are invalid.")
        except:
            return (False, "Must enter Login Credentials")
class TripManager(models.Manager):
    def trip_maker(self, postData):
        errors = []
        flag = False
        # diff =  postData['datefrom'] - postData['datenow']
        # print diff.days //date
        if not postData['destination']:
            errors.append('Please enter a destination')
            flag = True
        if not postData['description']:
            errors.append('Please enter a description')
            flag = True
        if not postData['datefrom']:
            errors.append('Please enter a travel date')
            flag = True
        elif postData['datefrom'].date() < postData['datenow'].date():
            errors.append('Travel date cannot be before today')
            flag = True
        if not postData['dateto']:
            errors.append('Please enter a return date')
            flag = True
        elif postData['dateto'].date() < postData['datefrom'].date():
            errors.append('Return date cannot be before Travel date')
            flag = True
        if flag:
            return (flag, errors)
        else:
            trip = Trip.objects.create(destination = postData['destination'], description= postData['description'], datefrom=postData['datefrom'], dateto=postData['dateto'], user = postData['user'])
            return (flag, trip)

class User(models.Model):

    name = models.CharField(max_length = 255)
    uname = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add =True)
    updated_at = models.DateTimeField(auto_now =True)
    objects = UserManager()


class Trip(models.Model):
    destination = models.TextField(max_length = 1000)
    description = models.TextField(max_length = 1000)
    datefrom =models.DateTimeField()
    dateto =models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add =True)
    updated_at = models.DateTimeField(auto_now =True)
    user = models.ForeignKey(User, blank = True)
    objects = TripManager()

class All_Trip(models.Model):
    user = models.ForeignKey(User)
    trip = models.ForeignKey(Trip)
    created_at = models.DateTimeField(auto_now_add =True)
    updated_at = models.DateTimeField(auto_now =True)
 # Trip.User.name.filter()
