# from multiprocessing import context
import email
from django.views import View
from urllib import request
from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from .forms import PaymentFrom
from .paytm import generate_checksum, verify_checksum
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.conf import settings

def index_paytm(request):
    form = PaymentFrom()
    return render(request, "index_paytm.html", {'form': form})

## payment views
@csrf_exempt
def initiate_payment(request):
    try:
        amount = int(request.POST['Amount'])
    except Exception as e:
        print(e)
        return render(request, 'index.html')

    transaction = Transaction.objects.create(made_by=request.POST['Name'], amount=amount)
    transaction.save()
    merchant_key = settings.PAYTM_SECRET_KEY

    params = (
        ('MID', settings.PAYTM_MERCHANT_ID),
        ('ORDER_ID', str(transaction.order_id)),
        ('CUST_ID', str(transaction.made_by)),
        ('TXN_AMOUNT', str(transaction.amount)),
        ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
        ('WEBSITE', settings.PAYTM_WEBSITE),
        # ('EMAIL', request.user.email),
        # ('MOBILE_N0', '9911223388'),
        ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
        ('CALLBACK_URL', 'http://localhost:8000/callback/'),
        # ('PAYMENT_MODE_ONLY', 'NO'),
    )

    paytm_params = dict(params)
    checksum = generate_checksum(paytm_params, merchant_key)

    transaction.checksum = checksum
    transaction.save()

    paytm_params['CHECKSUMHASH'] = checksum
    print('SENT: ', checksum)
    return render(request, 'redirect.html', context=paytm_params)

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        received_data = dict(request.POST)
        paytm_params = {}
        paytm_checksum = received_data['CHECKSUMHASH'][0]
        for key, value in received_data.items():
            if key == 'CHECKSUMHASH':
                paytm_checksum = value[0]
            else:
                paytm_params[key] = str(value[0])
        # Verify checksum
        is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
        if is_valid_checksum:
            received_data['message'] = "Checksum Matched"
            msg = 'Your payment made successfully done.'
        else:
            msg = 'Your payment failed. Please try again later.'
            received_data['message'] = "Checksum Mismatched"
            return render(request, 'callback.html', context=received_data)
        #return render(request, 'mycart.html', context=received_data)
        return redirect('index')


def login_page(request):
    
    return render(request, 'login.html')

def login(request):
    # print(request.POST)
    try:
        master = Master.objects.get(email=request.POST['email'])
        if master.password == request.POST['password']:
            request.session['email'] = master.email
            return redirect(index)
        else:
            return redirect(login_page)
    except Master.DoesNotExist as Err:
        print("Record Not Found")
        
    return redirect(register_page)




def register_page(request):
    return render(request, "register.html")

def register(request):
    email = request.POST['email']
    password = request.POST['password']

    profile = Master.objects.create(email=email, password=password)
    profile.save()

    return redirect(login_page)


def logout_page(request):
    if 'email' in request.session:
        auth_logout(request)
    return redirect(login_page)

def profile_page(request):
    if 'email' in request.session:
        profile = Master.objects.get(email=request.session['email'])
        context = {
            'profile' : profile
        }
        return render(request, 'profile.html', context)

def update_data(request):

    profile = Master.objects.get(email=request.session['email'])


    profile.f_name = request.POST['f_name']
    profile.location = request.POST['location']


    profile.save()


    return redirect(profile_page)

def upload_image(request):
    profile = Master.objects.get(email=request.session['email'])

    if 'image' in request.FILES:
        profile.profileimage = request.FILES['image']
        profile.save()

    return redirect(profile_page)


def change_password(request):
    profile = Master.objects.get(email=request.session['email'])

    if profile.password == request.POST['cpass']:
        profile.password = request.POST['npass']
        profile.save()
        return redirect(login_page)
    else:
        messages.info(request, "Current Password is incorrect")
        return redirect(login_page)
            


def index(request):
    if 'email' in request.session:
        profile = Master.objects.get(email=request.session['email'])

        service_data = Service.objects.all()

        context = {
            'profile' : profile,
            'service_data' : service_data,
        }

        return render(request, "index.html", context)
    else:
        return redirect(login_page)


def service_page(request):
    if 'email' in request.session:
        profile = Master.objects.get(email=request.session['email'])
        
        service_data = Service.objects.all()

        context = {
            'profile' : profile,
            'service_data' : service_data,
        }

        return render(request, "service.html", context)



class ServiceDetailView(View):
    def get(self, request, pk):
        if 'email' in request.session:
            profile = Master.objects.get(email=request.session['email'])
            service_data = Service.objects.get(pk=pk)

            context = {
                'profile' : profile,
                'service_data' : service_data
            }

            return render(request, 'single.html', context)

def add_to_cart(request):
    if 'email' in request.session:
        profile = Master.objects.get(email=request.session['email'])
        service_id = request.GET.get('serv_id')
        service = Service.objects.get(id=service_id)

        OrderedService(master=profile, service=service).save()
        context = {
            'service' : service,
            'profile' : profile
        }
        return render(request, 'cart.html', context)