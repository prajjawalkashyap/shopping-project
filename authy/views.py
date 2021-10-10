from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .models import User, Address
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from .utils import generate_token
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
def loginPage(request):
    if not request.user.is_authenticated:
        return render(request, 'auth/login.html')
    else:
        return redirect('/')


def logging(request):
    if request.method == 'POST':
        mail = request.POST.get('email', '')
        user_password = request.POST.get('password', '')
        user = authenticate(username=mail, password=user_password)

        if user is not None:
            login(request, user)
            messages.success(request,'Login successful')
            return redirect('/')
        else:
            messages.success(request, 'Incorrect credentials')
            return redirect('/auth/login')


def registration(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        userCheck = User.objects.filter(email=email)
        phone = request.POST.get('phone')
        userPhone = User.objects.filter(phone=phone)
        if userCheck or userPhone:
            messages.error(request, 'User with same phone number or email already registered')
            return redirect('/auth/register/')
        else:
            name = request.POST.get('name')
            dob = request.POST.get('dob')
            password = request.POST.get('password')
            user_obj = User.objects.create_user(first_name=name, phone=phone, password=password,
                                                   email=email, user_name=email, dob=dob)
            user_obj.save()

            current_site = get_current_site(request)
            email_sub = "Activate your account"

            message = render_to_string('auth/activate.html',
                                       {
                                           'user': user_obj,
                                           'domain': current_site.domain,
                                           'uid': urlsafe_base64_encode(force_bytes(user_obj.pk)),
                                           'token': generate_token.make_token(user_obj),
                                       })
            email = EmailMultiAlternatives(
                subject=email_sub,
                body='',
                from_email=settings.EMAIL_HOST_USER,
                to=[email]
            )
            email.attach_alternative(message, "text/html")
            try:
                email.send()
                messages.success(request,'Activate your account to login')
                return redirect('/auth/login')
            except:
                messages.error(request, 'Unknown error occurred')
                return redirect('/auth/register')


def user_logout(request):
    logout(request)
    messages.success(request,'Logout')
    return redirect('/auth/login')


def activateView(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except:
        user = None
    if user is not None and generate_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request,'Account activated')
        return redirect('/')
    else:
        messages.error(request,'Unknown error occurred')
        return redirect('/auth/register')


@login_required
def addAddress(request):
    if request.method == 'POST':
        address = request.POST.get('address')
        addType = request.POST.get('type')
        state = request.POST.get('state')
        pinCode = request.POST.get('zip')
        add = Address(
            user=request.user,
            address=address,
            type=addType,
            pin=pinCode,
            state=state
        )
        add.save()
        messages.success(request,'Address added')
        return redirect('/checkout')

@login_required
def account(request):
    return render(request, 'auth/account.html')
