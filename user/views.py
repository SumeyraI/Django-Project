from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages

# Create your views here.
from content.models import Menu, Content, ContentForm, ContentImageForm, CImages
from food.models import Category, Comment
from home.models import UserProfile
from order.models import Order, OrderProduct
from user.forms import UserUpdateForm, ProfileUpdateForm

@login_required(login_url='/login')
def index(request):
    category = Category.objects.all()
    current_user = request.user
    profile = UserProfile.objects.get(user_id=current_user.id)


    context = {
        'category': category,
        'profile': profile
    }

    return render(request, 'user_profile.html', context)

@login_required(login_url='/login')
def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)

        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Hesabınız başarılı bir şekilde güncellenmiştir !")
            return redirect("/user")

    else:
        category = Category.objects.all()
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)
        context = {
            'category': category,
            'user_form': user_form,
            'profile_form': profile_form,
        }
        return render(request, 'user_update.html', context)

@login_required(login_url='/login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Şifreniz başarılı bir şekilde güncellenmiştir !")
            return HttpResponseRedirect("/user")
        else:
            messages.error(request, 'Please correct the error below!<br>'+ str(form.errors))
            return HttpResponseRedirect("/user/password")
    else:
        category = Category.objects.all()
        form = PasswordChangeForm(request.user)
        return render(request, 'change_password.html', {
            'form': form, 'category': category
        })

@login_required(login_url='/login')
def orders(request):
    category = Category.objects.all()
    current_user = request.user
    orders = Order.objects.filter(user_id=current_user.id)
    context = {
        'category': category,
        'orders': orders,
    }
    return render(request, 'user_orders.html', context)

@login_required(login_url='/login')
def orderdetail(request,id):
    category = Category.objects.all()
    current_user = request.user
    order = Order.objects.get(user_id=current_user.id, id=id)
    orderitems = OrderProduct.objects.filter(order_id=id)
    context = {
        'category': category,
        'order': order,
        'orderitems': orderitems,
    }
    return render(request, 'user_order_detail.html', context)

@login_required(login_url='/login')
def comments(request):
    category = Category.objects.all()
    current_user = request.user
    comments = Comment.objects.filter(user_id=current_user.id)
    context = {
        'category': category,
        'comments': comments,

    }
    return render(request, 'user_comments.html', context)

@login_required(login_url='/login')
def deletecomment(request,id):
    current_user = request.user
    Comment.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request, 'Your comment deleted success!')

    return HttpResponseRedirect('/user/comments')

@login_required(login_url='/login')
def contents(request):
    category = Category.objects.all()
    menu = Menu.objects.all()
    current_user = request.user
    contents = Content.objects.filter(user_id=current_user.id)
    context = {
        'category': category,
        'menu': menu,
        'contents': contents,

    }

    return render(request, 'user_contents.html', context)

@login_required(login_url='/login')
def addcontent(request):
    if request.method == 'POST':
        form = ContentForm(request.POST, request.FILES)
        if form.is_valid():
            current_user = request.user
            data = Content()
            data.user_id = current_user.id
            data.title = form.cleaned_data['title']
            data.keywords = form.cleaned_data['keywords']
            data.description = form.cleaned_data['description']
            data.image = form.cleaned_data['image']
            data.type = form.cleaned_data['type']
            data.slug = form.cleaned_data['slug']
            data.detail = form.cleaned_data['detail']
            data.status = 'False'
            data.save()
            messages.success(request, 'Your Content Inserted Successfully')
            return HttpResponseRedirect('/user/contents')
        else:
            messages.success(request, 'Content Form Error :' + str(form.errors))
            return HttpResponseRedirect('/user/addcontent')
    else:
        category = Category.objects.all()
        menu = Menu.objects.all()
        form = ContentForm()
        context = {
            'category': category,
            'menu': menu,
            'form': form,

        }
        return render(request, 'user_addcontent.html', context)

@login_required(login_url='/login')
def contentedit(request,id):
    content = Content.objects.get(id=id)
    if request.method == 'POST':
        form = ContentForm(request.POST, request.FILES, instance=content)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your Content Updated Successfully')
            return HttpResponseRedirect('/user/contents')
        else:
            messages.success(request, 'Content Form Error :' + str(form.errors))
            return HttpResponseRedirect('/')
    else:
        category = Category.objects.all()
        menu = Menu.objects.all()
        form = ContentForm(instance=content)
        context = {
            'category': category,
            'menu': menu,
            'form': form,

        }
        return render(request, 'user_addcontent.html', context)

@login_required(login_url='/login')
def contentdelete(request,id):
    current_user = request.user
    Content.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request, 'Content deleted..')
    return HttpResponseRedirect('/user/contents')


def contentaddimage(request,id):
    if request.method == 'POST':
        lasturl=request.META.get('HTTP_REFERER')
        form = ContentImageForm(request.POST, request.FILES)
        if form.is_valid():
            data = CImages()
            data.title = form.cleaned_data['title']
            data.content_id = id
            data.image = form.cleaned_data['image']
            data.save()
            messages.success(request, 'Your Image Uploaded Successfully')
            return HttpResponseRedirect(lasturl)
        else:
            messages.success(request, 'Content Form Error :' + str(form.errors))
            return HttpResponseRedirect(lasturl)

    else:
        content = Content.objects.get(id=id)
        images = CImages.objects.filter(content_id=id)
        form = ContentImageForm()
        context = {
            'content': content,
            'images': images,
            'form': form,

        }
        return render(request, 'content_gallery.html', context)
