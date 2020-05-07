from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from food.models import Food, Category, Images
from home.models import Setting, ContactFormu, ContactFormMessage


def index(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    sliderdata = Food.objects.all()[:10]

    dayproducts = Food.objects.all()[:4]
    lastproducts = Food.objects.all().order_by('-id')[:4]
    randomproducts = Food.objects.all().order_by('?')[:4]




    context = {'setting': setting,
               'page':'home',
               'category':category,
               'sliderdata':sliderdata,
               'dayproducts':dayproducts,
               'lastproducts':lastproducts,
               'randomproducts':randomproducts
               }
    return render(request, 'index.html', context)

def hakkimizda(request):
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting}
    return render(request, 'hakkimizda.html', context)

def referanslar(request):
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting}
    return render(request, 'referanslarimiz.html', context)

def iletisim(request):

    if request.method == 'POST':
        form = ContactFormu(request.POST)
        if form.is_valid():
            data = ContactFormMessage()
            data.name = form.cleaned_data['name']
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(request, "Mesajınız başarı ile gönderilmiştir. Teşekkürler")
            return HttpResponseRedirect ('/iletisim')


    setting = Setting.objects.get(pk=1)
    form = ContactFormu()
    context = {'setting': setting, 'form' : form}
    return render(request, 'iletisim.html', context)

def category_products(request,id,slug):
    category = Category.objects.all()
    categorydata = Category.objects.get(pk=id)
    products = Food.objects.filter(category_id=id)
    context = {'products': products,
               'category': category,
               'categorydata': categorydata

               }
    return render(request,'products.html',context)


def product_detail(request,id,slug):
    category = Category.objects.all()
    product = Food.objects.get(pk=id)
    images = Images.objects.filter(food_id=id)
    context = {'product': product,
               'category': category,
               'images': images,
               }
    return render(request,'product_detail.html',context)