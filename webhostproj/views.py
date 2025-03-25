from urllib.parse import urlencode
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import usersForm
from service.models import UsersForm
from service.models import Service
from news.models import News
from contact.models import Contact
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.core.mail import send_mail
from django.http import HttpResponse


data={
    'title':'Home Page',
    'bdata':'WelCome to my home page | Subin Manandhar.',
    'clist':['PHP','Java','Django'],
    'numbers':[10,20,30,40,50],
    'student_details':[
        {'name':'Pradeep','phone':9800000089},
         {'name':'Sachin','phone':9800980098}
        ]

}

def homePage(request):
    newsData = News.objects.all()
    serviceData = Service.objects.all().order_by('-service_title') 

    # Filtering service data if 'servicename' is provided
    st = request.GET.get('servicename')
    if st:
        serviceData = serviceData.filter(service_title__icontains=st)

    # Pagination
    paginator = Paginator(serviceData, 2)
    page_number = request.GET.get('page')

    try:
        serviceDataFinal = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page.
        serviceDataFinal = paginator.page(1)
    except EmptyPage:
        # If page is out of range (too high or <1), deliver last page.
        serviceDataFinal = paginator.page(paginator.num_pages)

    totalpage = paginator.num_pages

    data = {
        'serviceData': serviceDataFinal,
        'newsData': newsData,
        'totalPagelist': list(range(1, totalpage + 1))  # Generates page numbers list
    }

    return render(request, "index.html", data)

# def aboutUs(request):
#      return render(request,"about.html")
def aboutUs(request):
    # Retrieve data from query parameters
    name = request.GET.get('name', '')
    email = request.GET.get('email', '')
    phone = request.GET.get('phone', '')

    user_data = {
        'name': name,
        'email': email,
        'phone': phone
    }

    return render(request, "about.html", {'user_data': user_data})

def contactUs(request):
     return render(request,"contact.html")

def saveEnquiry(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        if name and email and phone and message:
            try:
                contactdetails = Contact(name=name, email=email, phone=phone, message=message)
                contactdetails.save()
                return JsonResponse({"message": "Contact detail saved successfully.", "messageClass": "text-success", "status": "success"})
            except Exception as e:
                return JsonResponse({"message": "Contact detail save failed.", "messageClass": "text-danger", "status": "error"})
        else:
            return JsonResponse({"message": "All fields are required.", "messageClass": "text-danger", "status": "error"})

    return render(request, "contact.html")

def service(request):
    serviceData = Service.objects.all().order_by('-service_title')

    # Filtering data if 'servicename' is provided
    st = request.GET.get('servicename')
    if st:
        serviceData = serviceData.filter(service_title__icontains=st)

    # Pagination
    paginator = Paginator(serviceData, 2)
    page_number = request.GET.get('page')

    try:
        serviceDataFinal = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page.
        serviceDataFinal = paginator.page(1)
    except EmptyPage:
        # If page is out of range (too high or <1), deliver last page.
        serviceDataFinal = paginator.page(paginator.num_pages)

    totalpage = paginator.num_pages

    data = {
        'serviceData': serviceDataFinal,
        'lastpage': totalpage,
        'totalPagelist': list(range(1, totalpage + 1))  # Generates page numbers list
    }
    
    return render(request, "service.html", data)

def price(request):
     return render(request,"price.html")

def newsdetails(request,slug):
    newsdetails=News.objects.get(news_slug=slug)
    data={
        'newsdetails':newsdetails
    }
    return render(request, "newsdetails.html",data)

def course(request):
    return HttpResponse("Welcome to my course page.")

def courseDetails(request,courseid):
    return HttpResponse(courseid)

def userform(request):
    if request.method == "POST":
        form = usersForm(request.POST)  # Bind data to form
        if form.is_valid():  # Validate form
            # Get cleaned data (automatically escapes dangerous input)
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']

            # Save to database
            userdetails = UsersForm(name=name, email=email, phone=phone)
            userdetails.save()

            # Use urlencode to safely encode parameters in URL
            query_params = urlencode({'name': name, 'email': email, 'phone': phone})
            url = f"{reverse('about_us')}?{query_params}"
            return HttpResponseRedirect(url)
    else:
        form = usersForm()

    return render(request, "userform.html", {'form': form})

def submitform(request):
  if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')

        # Redirect to about-us with query parameters
        url = f"{reverse('about_us')}?name={name}&email={email}&phone={phone}"
        return HttpResponseRedirect(url)
  


def calculator(request):
    result = None  # Initialize result
    
    if request.method == "POST":
        try:
            # Ensure both fields are filled
            if not request.POST.get('num1') or not request.POST.get('num2'):
                return render(request, "calculator.html", {"error": "Please enter both numbers."})

            # Convert input safely
            n1 = float(request.POST.get('num1', 0))
            n2 = float(request.POST.get('num2', 0))
            opr = request.POST.get('opr')

            # Perform Calculation
            if opr == '+':
                result = n1 + n2
            elif opr == '-':
                result = n1 - n2
            elif opr == '*':
                result = n1 * n2
            elif opr == '/':
                if n2 == 0:
                    result = "Error: Division by zero"
                else:
                    result = n1 / n2
            else:
                result = "Invalid Operator"

        except ValueError:
            result = "Error: Invalid number input."
        except Exception as e:
            result = f"Error: {e}"  # Show error message

    return render(request, "calculator.html", {"result": result})


def send_email(request):
    subject = "Welcome to Django Email Sending"
    message = "Hello! This is a test email sent from Django."
    from_email = "manandharsubin20440803@gmail.com"  # Same as EMAIL_HOST_USER
    recipient_list = ["subin.syami@gmail.com"]  # Replace with actual recipient's email

    send_mail(subject, message, from_email, recipient_list)
    
    return HttpResponse("Email sent successfully!")
