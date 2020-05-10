from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from food.models import Category
from order.models import ShopCartForm, ShopCart


def index(request):
    return HttpResponse("order app")

@login_required(login_url='/login')
def addtocart(request,id):
    url = request.META.get('HTTP_REFERER')
    current_user = request.user

    checkproduct = ShopCart.objects.filter(product_id=id)
    if checkproduct:
        control = 1
    else:
        control = 0


    if request.method == 'POST':
        form = ShopCartForm(request.POST)
        if form.is_valid():
            if control==1:
                data = ShopCart.objects.get(product_id=id)
                data.quantity += form.cleaned_data['quantity']
                data.save() #veritabanına kaydeder.
            else: #sepette ürün yoksa.

                data = ShopCart()
                data.user_id = current_user.id
                data.product_id = id
                data.quantity = form.cleaned_data['quantity']
                data.save()
        request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()
        messages.success(request,"Ürün başarı ile sepete eklenmiştir. Teşekkürler..")
        return HttpResponseRedirect(url)

    else: #Ürün direkt sepete ekle butonuna basıldıysa bu if calisir
        if control == 1:
            data = ShopCart.objects.get(product_id=id)
            data.quantity += 1
            data.save()

        else:
            data = ShopCart()
            data.user_id = current_user.id
            data.product_id = id
            data.quantity = 1
            data.save()
            request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()
            messages.success(request, "Ürün başarı ile sepete eklenmiştir. Teşekkürler..")
            return HttpResponseRedirect(url)

    messages.warning(request,"Ürünü sepete eklemede hata oluştu. Lütfen kontrol ediniz. ")

    return HttpResponseRedirect(url)

@login_required(login_url='/login') #sepetten silme işlemi
def shopcart(request):
    category = Category.objects.all()
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()

    total=0
    for rs in shopcart:
        total += rs.product.price * rs.quantity

    context = {'shopcart': shopcart,
               'category': category,
               'total': total,
               }
    return render(request, 'Shopcart_products.html', context)

@login_required(login_url='/login')
def deletefromcart(request,id):
    ShopCart.objects.filter(id=id).delete()

    current_user = request.user
    request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()
    messages.success(request, "Ürün sepetten silinmiştir.")
    return HttpResponseRedirect("/shopcart")