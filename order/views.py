from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.utils.crypto import get_random_string

from food.models import Category, Food
from home.models import UserProfile
from order.models import ShopCartForm, ShopCart, OrderForm, Order, OrderProduct


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



@login_required(login_url='/login')
def orderproduct(request):  #siparis edilen urunu kaydediyoruz.
    current_user = request.user
    category = Category.objects.all()
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total=0
    for rs in shopcart:
        total += rs.quantity * rs.product.price


    if request.method == 'POST':
        form = OrderForm(request.POST)
        # check whether it's valid:
        if form.is_valid():

            # Send Credit card information to bank and get result
            # If payment accepted continue else send payment error to checkout page

            data = Order()
            data.first_name = form.cleaned_data['first_name'] #get product quantity from form
            data.last_name = form.cleaned_data['last_name']
            data.address = form.cleaned_data['address']
            data.city = form.cleaned_data['city']
            data.phone = form.cleaned_data['phone']
            data.user_id = current_user.id
            data.total = total
            data.ip = request.META.get('REMOTE_ADDR')
            ordercode = get_random_string(5).upper()
            data.code = ordercode
            data.save()

            shopcart = ShopCart.objects.filter(user_id=current_user.id)
            for rs in shopcart:
                detail = OrderProduct()
                detail.order_id     = data.id # Order Id
                detail.product_id   = rs.product_id
                detail.user_id      = current_user.id
                detail.quantity     = rs.quantity
                #  Reduce product Amount  (quantity)
                detail.price = rs.product.price
                detail.amount = rs.amount
                detail.save()

                product = Food.objects.get(id=rs.product_id)
                product.amount -= rs.quantity #urunu stoktan sayısını azalttık
                product.save()

            ShopCart.objects.filter(user_id=current_user.id).delete() # Clear & Delete shopcart
            request.session['cart_items']=0
            messages.success(request, "Your Order has been completed. Thank You ")
            return render(request, 'Order_Completed.html',{'ordercode':ordercode,'category':category})
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect("/order/orderproduct")

    form = OrderForm()
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {'form': form,
               'category':category,
               'shopcart': shopcart,
               'total': total,
               'profile':profile,
               }
    return render(request, 'Order_Form.html', context)