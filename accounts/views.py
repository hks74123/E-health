import django
from django.db.models.query import InstanceCheckMeta
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.decorators import login_required
from .models import Host, Meeting
from .forms import *
import datetime
import requests
import json
from datetime import date, timezone
import smtplib
import datetime
from email.message import EmailMessage
from random import choice
from django.conf import settings
from datetime import timedelta
from django.utils import timezone
import time

# Create your views here.

@login_required(login_url='/admin_login/')
def dashboard(request):
    if request.method=='POST':
        des=request.POST['typedoc']
        if(des=='None'):
            h = Host.objects.all()
            hosts = sorted(list(h),key=lambda x: x.host_name)
            parameters = {'hosts':hosts}
            return render(request,'dashboard.html',parameters)
        else:
            h = Host.objects.filter(host_desc=des)
            hosts = sorted(list(h),key=lambda x: x.host_name)
            parameters = {'hosts':hosts}
            return render(request,'dashboard.html',parameters)
    h = Host.objects.all()
    hosts = sorted(list(h),key=lambda x: x.host_name)
    c_time=timezone.now()
    deltime=timedelta(hours=5,minutes=30)
    c_time=c_time+deltime
    if(c_time.hour==9):
        timeformat = 't'+ '0'+str(c_time.hour) + 'to' + str(int(c_time.hour)+1)
    else:
        timeformat = 't'+ str(c_time.hour) + 'to' + str(int(c_time.hour)+1)
    parameters = {'hosts':hosts}
    tod_day=datetime.datetime.today().weekday()
    if(int(c_time.hour)<9 or int(c_time.hour)==12):
        for i in h:
            a=i.available.split("-")[0]
            b=i.available.split("-")[1]
            a_t=time.strptime(a, "%A").tm_wday
            b_t=time.strptime(b, "%A").tm_wday
            if(tod_day>=a_t and tod_day<=b_t):
                i.status=True
            else:
                i.status=False
    elif(int(c_time.hour)>=17):
        for i in h:
            t_day=tod_day+1
            a=i.available.split("-")[0]
            b=i.available.split("-")[1]
            a_t=time.strptime(a, "%A").tm_wday
            b_t=time.strptime(b, "%A").tm_wday
            if(t_day>=a_t and t_day<=b_t):
                i.status=True
            else:
                i.status=False
    else:
        for i in h:
            if(getattr(i,timeformat)==True):
                a=i.available.split("-")[0]
                b=i.available.split("-")[1]
                a_t=time.strptime(a, "%A").tm_wday
                b_t=time.strptime(b, "%A").tm_wday
                if(tod_day>=a_t and tod_day<=b_t):
                    i.status=True
                else:
                    i.status=False
            else:
                i.status=False
    return render(request,'dashboard.html',parameters)
 
## Verifies that only Admin uses these options and redirects them to required webpage respectively
def verify(request):
    if request.method == 'POST':
        key = request.POST.get('password')
        user = auth.authenticate(username=request.user.username,password=key)
        if user is not None:
            if request.POST.get('profile'):
                user_prof=profile_details.objects.get(user=user)
                form = Add_profile1(instance=user_prof)
                return render(request, 'profile_manager.html', {'form' : form})

            if request.POST.get('logout'):
                auth.logout(request)
                return redirect('/')

            if request.POST.get('meeting'):
                meetings = Meeting.objects.filter(date = datetime.datetime.now())
                m = reversed(list(meetings))
                info = {'meeting':m}
                return render(request, 'meeting_history.html',info)
        
        # When wrong password is given
        else:
            messages.warning(request,'Please enter valid credentials !!')
            return redirect('/dashboard')

    else:
        return redirect('/dashboard')

@login_required(login_url='/admin_login/')
def meeting_manager(request):
    if request.method == 'POST':

        # If visitor button is clicked, visitor details are shown
        if request.POST.get("visitor"): 
            meeting_id = request.POST.get("visitor")
            meeting = Meeting.objects.get(id = meeting_id)
            host = Host.objects.get(current_meeting_id = meeting_id)
            meeting_details = {'meeting' : meeting, 'host' : host}
            return render(request, 'visitor_details.html', meeting_details)

        # Opens the meeting form
        elif request.POST.get("meeting"): 
            host_id = request.POST.get("meeting")
            host = Host.objects.get(id = host_id)
            form = Meeting_form()
            param = {'form':form,'host':host}
            return render(request, 'meeting_form.html', param)

    else:
        return redirect('/dashboard')

# Saves the visitor details filled in meeting form
@login_required(login_url='/admin_login/')
def save_meeting(request):
    if request.method == 'POST':
        host_name = request.POST['host']
        tslot=request.POST['fixslot']
        host = Host.objects.get(host_name=host_name)
        form = Meeting_form(request.POST)
        c_time=timezone.now()
        deltime=timedelta(hours=5,minutes=30)
        c_time=c_time+deltime
        if form.is_valid():
            if(getattr(host,tslot)==False):
                messages.error(request,f'Sorry for this doctor {tslot} is booked try another slot !!')
                return redirect('/dashboard')

            if(int(c_time.hour)>=17 or int(c_time.hour)>=int(tslot[4:])):
                c_meeting=Meeting.objects.filter(host=host_name,time_slott=tslot,date=datetime.date.today()+timedelta(1))
            else:
                c_meeting=Meeting.objects.filter(host=host_name,time_slott=tslot,date=datetime.date.today())
            if(len(c_meeting)==14):
                getattr(host,tslot)==False
            slot=(tslot[1]+tslot[2])+':'+str(4*(len(c_meeting)))
            hour,minut=map(int,slot.split(':'))
            timenow=datetime.time(hour=hour,minute=minut)
            timetill=datetime.time(hour=hour,minute=minut+4)
            instance = form.save(commit=False)
            instance.host = host_name
            instance.time_slott=str(tslot)
            instance.time_in=timenow
            instance.time_out=timetill
            if(int(c_time.hour)>=17 or int(c_time.hour)>=int(tslot[4:])):
                instance.date=datetime.date.today()+timedelta(1)
            instance.save()
            h_id=host.id
            visitors_name=instance.visitor_name
            visitors_email=instance.visitor_email
            
                
            rec = [host.host_email]
                
            ## EMAIL AND SMS TO HOST
            status=send_mail(rec,visitors_name,visitors_email,h_id,slot,host_name)
            # sendsms(subject,visitor,host)
            messages.success(request,'Information sent to Host, You will be called shortly !!')
            return redirect('/dashboard')
        else:
            pass
    else:
        return redirect('/dashboard')

## Checkout function when Host clicks checkout button
def checkout(request):
    if request.method == 'GET':
        meeting_id = request.GET['mid']
        meeting = Meeting.objects.get(id = meeting_id)
        host = next(iter(Host.objects.filter(current_meeting_id=meeting_id)), None)
        # If checkout button already clicked
        if (meeting.time_out != None) and (host==None):
            return HttpResponse(meeting.visitor_name+', Already Checked Out !!')
        host.status = True
        host.current_meeting_id = None 
        meeting.time_out = datetime.datetime.now()
        host.save()
        meeting.save()
        rec = [meeting.visitor_email]
        # sending email to visitor
        email(rec,host)
        return HttpResponse(meeting.visitor_name+', Checked Out Successfully !!')

# profile manager that saves host profile
@login_required(login_url='/admin_login/')
def profile_manager(request):
    if request.method=='POST':
        form = Add_profile(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/dashboard')
    else:
        return redirect('/dashboard')

# Checks for the given id in host database and fills the add profile form automatically with it
@login_required(login_url='/admin_login/')
def edit_profile(request):
    if request.method == 'POST':
        host_id = request.POST.get('editing')
        instance = Host.objects.filter(id=host_id).first()
        form = Add_profile(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('/dashboard')
    else:
        return redirect('/dashboard')

# checks which button was clicked, either edit or delete and redirects them respectively
@login_required(login_url='/admin_login/')
def edit_delete(request):
    if request.method=='POST':
        host_id =request.POST.get('id')
        if host_id=='':
            # If invalid profile id was given
            messages.warning(request,'Please enter a valid profile Id first !!')
            form = Add_profile()
            return render(request, 'profile_manager.html', {'form' : form})
        host = Host.objects.filter(id=host_id).first()
        if host:
            if request.POST.get('edit'):
                form = Add_profile(instance=host)
                context = {'form':form,'edit':True,'info':host_id}
                return render(request, 'profile_manager.html',context)
            elif request.POST.get('delete'):
                host.delete()
                return redirect('/dashboard')
        else:
            # If no profile was found
            messages.warning(request,'Profile not found !!')
            form = Add_profile()
            return render(request, 'profile_manager.html', {'form' : form})
    else:
        return redirect('/dashboard')


# Sends the email to both host and visitor

def send_mail(to,name,visitors_email,h_id,slot,host_name):
    s=slot
    s1=int(slot[3:])+4
    sender_mail = "no.reply.detailsender@gmail.com"
    password_sender = "madda@guddu"
    message = EmailMessage()
    message['To'] = [to,visitors_email]
    message['From'] = sender_mail
    message['Subject'] = "You have a visitor"
    message.set_content(
        f"User {name} booked a slot with {host_name} in time slot {s} to {s[:2]}:{s1}")
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_mail, password_sender)
        server.send_message(message)
        return True         
    except:
        return False 






# def email(subject,visitor,rec,host=None):
#     ## FILL IN YOUR DETAILS HERE
#     sender = 'hemant91852@gmail.com'
#     if host:
#         html_content = render_to_string('visitor_mail_template.html', {'visitor':visitor,'host':host}) # render with dynamic value
#     else:
#         html_content = render_to_string('host_mail_template.html', {'visitor':visitor}) # render with dynamic value
#     text_content = strip_tags(html_content)

#     # try except block to avoid wesite crashing due to email error
#     try:
#         msg = EmailMultiAlternatives(subject, text_content, sender, rec)
#         msg.attach_alternative(html_content, "text/html")
#         msg.send()
#     except:
#         pass
#     return

# # Sends the SMS to host
# def sendsms(subject,visitor,host):
#     URL = 'https://www.way2sms.com/api/v1/sendCampaign'
#     msg = "Hey, "+host.host_name+", Your Upcoming meeting is with : "+visitor.visitor_name+", Contact no. : "+str(visitor.visitor_phone)+", Email Id : "+visitor.visitor_email+". Check-In Time is : "+str(visitor.time_in)[11:16]
#     ## FILL IN YOUR DETAILS HERE
#     req_params = {
#     'apikey':'your api key',
#     'secret':'your secret key',
#     'usetype':'stage',
#     'phone': '+91'+str(host.host_phone),
#     'message':msg,
#     'senderid':'your way2sms account email id'
#     }
#     # try except block to avoid wesite crashing due to SMS error
#     try:
#         requests.post(URL, req_params)
#     except:
#         pass
#     return

def profile_managered(request):
    if request.method=='POST':
        user_obj1=profile_details.objects.get(u_nm=request.user.username)
        user=User.objects.get(username=request.user.username)
        f_name=request.POST.get('fstname')
        u_name=request.POST.get('usernm')
        u_maill=request.POST.get('maill')
        if(f_name!=None):
            user_obj1.fstname=f_name
        if(u_name!=None):
            user_obj1.u_nm=u_name
        if(u_maill!=None):
            user_obj1.urmail=u_maill
        user_obj1.id=user_obj1.id
        user_obj1.save()
        user_prof=profile_details.objects.get(user=user)
        form = Add_profile1(instance=user_prof)
        return render(request, 'profile_manager.html', {'form' : form})
    else:
        return redirect('/dashboard')