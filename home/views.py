import json

from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from content.models import Menu, Content, CImages
from food.models import Food, Category, Images, Comment
from home.forms import SearchForm, SignUpForm
from home.models import Setting, ContactFormu, ContactFormMessage, UserProfile
from order.models import ShopCart


def index(request):
    current_user = request.user
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    menu = Menu.objects.all()
    sliderdata = Food.objects.all()[:10]
    dayproducts = Food.objects.all()[:4]
    lastproducts = Food.objects.all().order_by('-id')[:4]
    randomproducts = Food.objects.all().order_by('?')[:4]
    request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()
    gift = Content.objects.filter(type='HEDİYE').order_by('-id')[:4]
    kampanya = Content.objects.filter(type='KAMPANYA').order_by('-id')[:4]

    context = {'setting': setting,
               'page':'home',
               'menu': menu,
               'kampanya': kampanya,
               'gift': gift,
               'category':category,
               'sliderdata':sliderdata,
               'dayproducts':dayproducts,
               'lastproducts':lastproducts,
               'randomproducts':randomproducts
               }
    return render(request, 'index.html', context)

def hakkimizda(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    context = {'setting': setting,
               'category': category,
               }
    return render(request, 'hakkimizda.html', context)

def referanslar(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    context = {'setting': setting,
               'category': category,
               }
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

    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    form = ContactFormu()
    context = {'setting': setting,
               'category': category,
               'form': form}
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
    comments = Comment.objects.filter(food_id=id,status='True')
    context = {'product': product,
               'comments': comments,

               'category': category,
               'images': images,
               }
    return render(request,'product_detail.html',context)


def product_search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():


            query = form.cleaned_data['query']
            catid = form.cleaned_data['catid']

            if catid == 0:
                products = Food.objects.filter(title__icontains=query)
            else:
                products = Food.objects.filter(title__icontains=query,category_id=catid)


            category = Category.objects.all()
            context = {'products': products,
                       'category': category,
                       'query': query,

                       }
            return render(request, 'products_search.html', context)

        return HttpResponseRedirect('/')


def search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        places = Food.objects.filter(title__icontains=q)
        results = []
        for rs in places:
            place_json = {}
            place_json = rs.title
            results.append(place_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


def login_view(request):
    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return HttpResponseRedirect('/')

        else:
            messages.warning(request, "Login Hatası ! Kullanıcı adı ya da şifre yanlış ")
            return HttpResponseRedirect('/login')


    category = Category.objects.all()
    context = {
        'category': category,
    }
    return render(request, 'login.html', context)


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            current_user = request.user
            data=UserProfile()
            data.user_id=current_user.id
            data.image="images/users/user.png"
            data.save()
            messages.success(request, "Hoş Geldiniz.. Sitemize başarılı bir şekilde üye oldunuz.Şimdiden afiyet olsun..")
            return HttpResponseRedirect('/')


    form = SignUpForm()
    category = Category.objects.all()
    context = {
        'category': category,
        'form': form,

    }

    return render(request, 'signup.html', context)


def menu(request,id):
    try:
        content = Content.objects.get(menu_id=id)
        link='/content/'+str(content.id)+'/menu'
        return HttpResponseRedirect(link)

    except:
        messages.warning(request, "Hata ! İlgili içerik buunamadı")
        link='/'
        return HttpResponseRedirect(link)

def contentdetail(request,id,slug):
    category = Category.objects.all()
    menu = Menu.objects.all()
    content = Content.objects.get(pk=id)
    images = CImages.objects.filter(content_id=id)

    context = {
        'category': category,
        'content': content,
        'menu': menu,
        'images': images,

    }
    return render(request, 'content_detail.html', context)
