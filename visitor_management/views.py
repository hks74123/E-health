# from django.http import HttpResponse
# from django.shortcuts import render, redirect
# from django.contrib.auth.models import User, auth
# from django.contrib.auth.decorators import login_required
# from accounts.models import Host

from typing import MutableSequence
from django.core.checks import messages
from django.http import request
from django.shortcuts import redirect, render,HttpResponse
from accounts.models import *
from django.contrib import messages
from django.contrib.auth.models import User,auth
from datetime import timezone
import smtplib
import datetime
from email.message import EmailMessage
from random import choice
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from accounts.forms import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

## Homepage
def home(request):
    return render(request, 'homepage.html')

## Doctors details for visitors
def doctors(request):
    hosts = Host.objects.all()
    parameters = {'hosts':hosts}
    return render(request,'doctors.html',parameters)

def generate_random_unicode():
        # logic to generate code
        varsptoken = ''
        alphas = ['-', '_', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        for i in range(26):
            alphas.append(chr(65+i))
            alphas.append(chr(97+i))
        for i in range(89):
            varsptoken += choice(alphas)

        return varsptoken

def send_mail(to, personalcode):
        # logic to send mail to user
    sender_mail = "no.reply.detailsender@gmail.com"
    password_sender = "madda@guddu"
    message = EmailMessage()
    message['To'] = to
    message['From'] = sender_mail
    message['Subject'] = "Welcome to E-HEALTH"
    message.set_content(
        f"Hello User welcome to E-HEALTH Your one time login link is\n {settings.SITE_URL}/confirm/{personalcode} \nvalid for next 15 minutes.")
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls() 
        server.login(sender_mail, password_sender)
        server.send_message(message)
        return True         # success 
    except:
        return False   


#meet_confirmation

def confirm_meet(request,pid):
    return render(request,'confirm.html', {'pid': pid})  

def confirmed_meet(request,pid):
    if request.method== 'POST':
        uname=request.POST['unamee']
        pass1=request.POST['passcode']
        me=profile_details.objects.filter(unicode=pid,)
        puser=User.objects.filter(username=uname)
        if len(me) != 1 or len(puser) != 1:
            return HttpResponse({'user not exists'})
        for person in me:
            if person.verified == 0:
                # match timestamp code here
                cur_time = datetime.datetime.now(timezone.utc)
                pre_time = person.timestamp
                del_time = str(cur_time-pre_time)
                del_time = del_time.split(':')
                if del_time[0] != '0':
                    # delete entry from database
                    profile_details.objects.filter(
                        unicode=pid).delete()
                    User.objects.filter(username=uname).delete()
                    return HttpResponse({'Time Limit Exceed'})
                elif int(del_time[1]) > 14:     # 15 minutes time
                    # delete entry from database
                    profile_details.objects.filter(
                        unicode=pid).delete()
                    User.objects.filter(username=uname).delete()
                    return HttpResponse({'Time limit Excced'})
                person.verified = 1
                person.unicode = None
                person.save()
                return HttpResponse({'success'})
            else:
                return HttpResponse({'Already Verified.'})
    elif request.user.is_authenticated:
        return redirect('/')
    else:
        return HttpResponse({'user is not authenticated.'})

    return render(request,'homepage.html')



## Login page for admin
def loginPage(request):
    if request.method== 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)

        if user is not None:
            datas = profile_details.objects.filter(user=user)
            for data in datas:
                if not data.verified:
                    messages.error(request,'User Not Verified Yet...')
                    return render(request, 'Singup.html')
            messages.info(request,'Logined Successfully!!')
            auth.login(request, user)
            return redirect("/dashboard")
        else:
            return redirect('/admin_login/')

    else:
        return render(request,'admin_login.html')
        
def Signupp(request):
    if request.method=='POST':
        first_name=request.POST['full_name']
        username=request.POST['username']
        email=request.POST['email']
        passw=request.POST['password']
        passw1=request.POST['password1']

        if passw==passw1:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username already exist')
                return redirect('/Signup')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'Email already exist')
                return redirect('/Signup')
            else:
                personalcode = generate_random_unicode()
                mytimecalculator = 0
                while(len(profile_details.objects.filter(unicode=personalcode))):
                    personalcode = generate_random_unicode()
                    mytimecalculator += 1
                    if mytimecalculator > 10000:
                # render(request,'logshower.html',{'formid':  'sorry but we are unable to process your request'})
                        pass 

                status = send_mail(email, personalcode)
                user=User.objects.create_user(username=username, password=passw, email=email, first_name=first_name)
                user.save();
                hkk=1
                upes = profile_details(user=user, urmail=email,u_nm= username,fstname=first_name,
                            unicode=personalcode, timestamp=datetime.datetime.now(timezone.utc))
                upes.save()
                messages.info(request,'Confirmation link sent to your mail')
                return render(request,'admin_login.html')
        else:
            messages.info(request,'Password not matching')
            return redirect('/Signup/')
    else:
        return render(request,'Singup.html')


# def docfilteration(request):
#     if request.method=='POST':
#         des=request.POST['typedoc']
#         if(des=='None'):
#             h = Host.objects.all()
#             hosts = sorted(list(h),key=lambda x: x.host_name)
#             parameters = {'hosts':hosts}
#             return render(request,'dashboard.html',parameters)
#         else:
#             h = Host.objects.filter(host_desc=des)
#             hosts = sorted(list(h),key=lambda x: x.host_name)
#             parameters = {'hosts':hosts}
#             return render(request,'dashboard.html',parameters)
#     else:
#         h = Host.objects.all()
#         hosts = sorted(list(h),key=lambda x: x.host_name)
#         parameters = {'hosts':hosts}
#         return render(request,'dashboard.html',parameters)

def forget_pass(request):
    if request.method=='POST':
        username=request.POST['username']
        u_obj=User.objects.filter(username=username)
        if u_obj is None:
            messages.info(request,'Username does not exist')
            return render(request,'Singup.html')
        else:
            datas = profile_details.objects.filter(u_nm=username)
            for data in datas:
                if not data.verified:
                    messages.info(request,'Username does not exist')
                    return render(request,'Singup.html')
                personal_code=generate_random_unicode()
                data.unicode=personal_code
                data.save()
                maill=data.urmail
                status=send_mail1(maill,personal_code)
                messages.info(request,'Password-Reset Link has been sent to your email')
                return render(request,'admin_login.html')

    return render(request,'send_reset_mail.html')

def send_mail1(to, personalcode):
        # logic to send mail to user
    sender_mail = "no.reply.detailsender@gmail.com"
    password_sender = "madda@guddu"
    message = EmailMessage()
    message['To'] = to
    message['From'] = sender_mail
    message['Subject'] = "Welcome to E-HEALTH"
    message.set_content(
        f"Hello User welcome to E-HEALTH Your password reset link is\n {settings.SITE_URL}/reset_pass/{personalcode} \nvalid for next 15 minutes.")
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls() 
        server.login(sender_mail, password_sender)
        server.send_message(message)
        return True         # success 
    except:
        return False  

def reset_pass(request,pid):
    if request.method=='POST':
        n_p=request.POST['New_Password']
        na_p=request.POST['Password_again']
        p_obj=profile_details.objects.filter(unicode=pid)
        for p_obj1 in p_obj:
            u_nam=p_obj1.u_nm
        u_obj=User.objects.filter(username=u_nam)
        if(n_p!=na_p):
            messages.info(request,'Password does not match')
            return redirect(f'/reset_pass/{pid}')
        for u_ob in u_obj:
            u_ob.set_password(n_p)
            u_ob.save()
        for ab in p_obj:
            ab.unicode=None
            ab.save()
        messages.info(request,'Password changed successfully!!')
        return redirect('/admin_login') 
    return render(request,'change_password.html', {'pid': pid})

@csrf_exempt
def doctor_login(request):
    if request.method=='POST':
        dd=request.POST['doc_id']
        name=request.POST['doc_name']
        user = auth.authenticate(username=dd,password=name)
        if user is not None:
            auth.login(request, user)
        else:
            messages.info(request,"Doctor Does not exists!!")
            return render(request,'doc_login.html')
        return redirect('/do_login')
    return render(request,'doc_login.html')
    
def checkout_doc_meet(request,pid):
    if request.method=='POST':
        dsd=pid[9:]
        dsd1=int(dsd)
        ddid=pid[:2]
        doc_obj=Host.objects.filter(id=ddid)
        get_bool=[]
        for docc in doc_obj:
            name1=docc.host_name
        for i in range(1,dsd1+1):
            dk=request.POST.get(f'chck{i}')
            get_bool.append(dk)

        
        for j in range(len(get_bool)):
            if(get_bool[j]=='on'):
                gt_id=request.POST.get(f'chck1{j+1}')
                c_o=Meeting.objects.filter(id=gt_id)
                for kk in c_o:
                    kk.checked_out=True
                    kk.save()
                    name1=kk.host
        
        meetings = Meeting.objects.filter(host=name1,date=datetime.date.today(),checked_out=False)
        m = reversed(list(meetings))
        ln=len(meetings)
        meetings1=Meeting.objects.filter(host=name1,date=datetime.date.today(),checked_out=True)
        m1 = reversed(list(meetings1))
        info = {'meeting':m,'pid':pid[:9],'lngth':ln,'meeting1':m1}
        return render(request,'doc_meeting.html',info)
    
    messages.info(request,'Please Login to proceed!!')
    return render(request,'doc_login.html')
@login_required(login_url='doc_login')
def doc_profile(request,pid):
    host_id=pid[:2]
    host = Host.objects.filter(id=host_id).first()
    form = Add_profile(instance=host)
    context = {'form':form,'edit':True,'info':host_id,'pid':pid}
    return render(request, 'doc_profilrmana.html',context)

    # get_dd=pid[:2]
    # host_obj=Host.objects.filter(id=get_dd)
    # info={'detials':host_obj}
    # return render(request,'doc_profilrmana.html',info)
@login_required(login_url='/doc_login/')
def profile_manager(request,pid):
    if request.method=='POST':
        host_id=pid[:2]
        instance = Host.objects.filter(id=host_id).first()
        form = Add_profile(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            host = Host.objects.filter(id=host_id).first()
            form = Add_profile(instance=host)
            context = {'form':form,'edit':True,'info':host_id,'pid':pid}
            messages.info(request,'Details Saved Successfully!!')
            return render(request, 'doc_profilrmana.html',context)
        else:
            messages.info(request,'Please fill out fields correctly!!')
            host = Host.objects.filter(id=host_id).first()
            form = Add_profile(instance=host)
            context = {'form':form,'edit':True,'info':host_id,'pid':pid}
            return render(request, 'doc_profilrmana.html',context)
    return redirect('/')
@login_required(login_url='/doc_login/')
def doc_meeths(request,pid):
    host_id=pid[:2]
    doc_obj=Host.objects.filter(id=host_id)
    for ob in doc_obj:
        host_name=ob.host_name

    meetings = Meeting.objects.filter(host=host_name,date=datetime.date.today(),checked_out=False)
    m = reversed(list(meetings))
    ln=len(meetings)
    meetings1=Meeting.objects.filter(host=host_name,date=datetime.date.today(),checked_out=True)
    m1 = reversed(list(meetings1))
    info = {'meeting':m,'pid':pid[:9],'lngth':ln,'meeting1':m1}
    return render(request,'doc_meeting.html',info)

def doc_logout(request):
    auth.logout(request)
    messages.info(request,'logged out sucessfully!!')
    return redirect('/doc_login')

def do_after_login(request):
    id=request.user.username
    dpc_obj=Host.objects.filter(id=id)
    for dk in dpc_obj:
        dd=dk.host_name
    name=dd
    dd1=id+'985jqry'
    if len(dpc_obj)!=0:
        meetings = Meeting.objects.filter(host=name,date=datetime.date.today(),checked_out=False)
        m = reversed(list(meetings))
        ln=len(meetings)
        meetings1=Meeting.objects.filter(host=name,date=datetime.date.today(),checked_out=True)
        m1 = reversed(list(meetings1))
        info = {'meeting':m,'pid':dd1,'lngth':ln,'meeting1':m1}
        return render(request,'doc_meeting.html',info)
    messages.info(request,"Doctor Does not exists!!")
    return render(request,'doc_login.html')