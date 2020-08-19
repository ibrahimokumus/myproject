from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from book.models import Category, Comment
from home.models import UserProfile, Setting
from order.models import OrderBook
from user.forms import UserUpdateForm, ProfileUpdateForm


@login_required(login_url='/login')
def index(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    current_user = request.user
    profile = UserProfile.objects.get(user_id=current_user.id)
    # return HttpResponse(profile)
    context = {
               'category': category,
                'profile': profile,
                'setting': setting,
               }
    return render(request, 'user_profile.html', context)

@login_required(login_url='/login')
def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST,instance=request.user)
        profile_form=ProfileUpdateForm(request.POST,request.FILES,instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,'your account has been updated')
            return redirect('/user')
    else:
        category = Category.objects.all()
        user_form = UserUpdateForm(instance=request.user)
        profile_form =ProfileUpdateForm(instance=request.user.userprofile)
        context = {
            'category': category,
            'user_form': user_form,
            'profile_form': profile_form,

        }
        return render(request,'user_update.html',context)


@login_required(login_url='/login')  # Check login
def change_password(request):
    setting = Setting.objects.get(pk=1)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated')
            return HttpResponseRedirect('/user')
        else:
            messages.error(request, 'Please correct the error below.<br>' + str(form.errors))
            return HttpResponseRedirect('/user/password')
    else:
        category = Category.objects.all()
        form = PasswordChangeForm(request.user)
        return render(request, 'change_password.html',
                      {
                          'form': form,
                          'category': category,
                          'setting': setting,
        })
@login_required(login_url='/login')  # Check login
def comments(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    current_user = request.user
    comments = Comment.objects.filter(user_id=current_user.id)
    context = {
        'category': category,
        'comments': comments,
        'setting': setting,
    }
    return render(request, 'user_comments.html', context)


@login_required(login_url='/login')  # Check login
def deletecomment(request, id):
    current_user = request.user
    Comment.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request, 'Comment delete..')
    return HttpResponseRedirect('/user/comments')


@login_required(login_url='/login')  # Check login
def orders(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    current_user = request.user
    orders = OrderBook.objects.filter(user_id=current_user.id)
    context = {
        'category': category,
        'orders': orders,
        'setting': setting,
    }
    return render(request, 'user_orders.html', context)


@login_required(login_url='/login')  # Check login
def orderdetail(request, id):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    current_user = request.user
    order = OrderBook.objects.get(user_id=current_user.id, id=id)
    orderitems = OrderBook.objects.filter(user_id=current_user.id)
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {
        'category': category,
        'order': order,
        'orderitems': orderitems,
        'profile': profile,
        'setting': setting,
    }
    return render(request, 'order_detail.html', context)
