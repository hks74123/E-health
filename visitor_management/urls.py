"""visitor_management URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('admin_login/', views.loginPage, name = 'admin_login'),
    path('doSignup/', views.Signupp, name = 'admin_signup'),
    path('Signup/', views.Signupp, name = 'admin_signup'),
    path('dashboard/', include('accounts.urls'), name = 'doctors'),
    path('doctors/', views.doctors, name = 'doctors'),
    path('confirm/<slug:pid>',views.confirm_meet,name='confirm_meet'),
    path('confirmed/<slug:pid>',views.confirmed_meet,name='confirmed_meet'),
    path('Forget_Pass/',views.forget_pass,name='pass-re'),
    path('reset_pass/<slug:pid>',views.reset_pass,name='pass-re-link'),
    path('doc_login/',views.doctor_login,name='doctor_login'),
    path('doc_profile/<slug:pid>/',views.doc_profile,name='doctor_profile'),
    path('checkout_doc_meet/<slug:pid>/',views.checkout_doc_meet,name='doc_meet_checker'),
    path('profile_manager/<slug:pid>/',views.profile_manager,name='doc_changeprof'),
    path('doc_meeths/<slug:pid>/',views.doc_meeths,name='Meet_hist'),
    path('doc_logout/',views.doc_logout,name='doctor_logout'),
    path('do_login/',views.do_after_login,name='login_it'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
