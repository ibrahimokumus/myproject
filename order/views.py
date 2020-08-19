from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.utils.crypto import get_random_string

from book.models import Category, Book
from home.models import Setting, UserProfile
from order.models import ShopCart, ShopCartForm, OrderForm, Order, OrderBook


def index(reuqest):
        return HttpResponse("Order page")

@login_required(login_url='/login')
def addtocart(request,id):
    url=request.META.get('HTTP_REFERER')
    current_user=request.user

    checkbook=ShopCart.objects.filter(book_id=id)
    if checkbook:
        control=1
    else:
        control=0
    if request.method=='POST':
        form=ShopCartForm(request.POST)
        if form.is_valid():
            if control==1:
               messages.success(request,"Ayni Kitaptan birden fazla alamazsiniz!")
            else:
                data = ShopCart()
                data.user_id = current_user.id
                data.book_id = id
                data.quantity=1
                data.save()
                request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()
                messages.success(request,"Ürün başarı ile sepete eklenmiştir.Teşekkür Ederiz")
        return  HttpResponseRedirect(url)
    else:
        if control == 1:
                messages.success(request, "Ayni Kitaptan birden fazla alamazsiniz!")
        else:
            data=ShopCart()
            data.user_id=current_user.id
            data.book_id=id
            data.quantity=1
            data.save()
            request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()
            messages.success(request,"Ürün başarı ile sepete eklenmiştir.Teşekkür Ederiz")
        return HttpResponseRedirect(url)
    
@login_required(login_url='/login')
def shopcart(request):
    category=Category.objects.all()
    current_user=request.user
    setting = Setting.objects.get(pk=1)
    shopcart=ShopCart.objects.filter(user_id=current_user.id)
    request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()


    context={'category':category,
             'shopcart':shopcart,
             'setting':setting,

             }
    return render(request,'Shopcart_books.html',context)

@login_required(login_url='/login')
def deletefromcart(request,id):
    category=Category.objects.all()
    setting = Setting.objects.get(pk=1)
    ShopCart.objects.filter(id=id).delete()
    current_user=request.user
    request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()
    messages.success(request, "Ürün sepetten silinmiştir")
    context={'category':category,
             'setting': setting,

             }
    return HttpResponseRedirect("/order/shopcart",context)

@login_required(login_url='/login')
def orderbook(request):
    category = Category.objects.all()
    current_user=request.user
    shopcart=ShopCart.objects.filter(user_id=current_user.id)



    if request.method =='POST':
        form = OrderForm(request.POST)

        if form.is_valid():
            data = Order()
            data.first_name=form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.address=form.cleaned_data['address']
            data.city=form.cleaned_data['city']
            data.phone=form.cleaned_data['phone']
            data.user_id=current_user.id

            data.ip=request.META.get('REMOTE_ADDR')
            ordercode=get_random_string(5).upper()
            data.code=ordercode
            data.save()

            #move shopcrt items for order books items
            shopcart=ShopCart.objects.filter(user_id=current_user.id)
            for rs in shopcart: #schopcart
                detail=OrderBook()
                detail.order_id   =data.id
                detail.book_id =rs.book_id
                detail.user_id    =current_user.id
                detail.quantity   =rs.quantity
                detail.stok_durum =rs.stok_durum
                detail.save()

                # ***************< Reduce >***************#
                book = Book.objects.get(id=rs.book_id)
                book.stok_durum -= rs.quantity
                book.save()
                #***************<^^^^^^^^^^>***************#

            ShopCart.objects.filter(user_id=current_user.id).delete()
            request.session['cart_items']=0
            messages.success(request,"Your order has been completed , thank you!" )
            return render(request,"Order_Complated.html",{'ordercode':ordercode,'category':category})
        else:
            messages.warning(request,form.errors)
            return HttpResponseRedirect("/order/orderbook")



    form = OrderForm()
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {'shopcart':shopcart,# hoca Schopcart yazmis
                'category': category,
                'profile': profile,
                'form':form,
               }

    return render(request,'Order_form.html',context)