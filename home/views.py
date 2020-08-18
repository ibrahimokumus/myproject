import json

from django.contrib.auth import authenticate, login, logout

from home.forms import SearchForm, SignUpForm
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

# Create your views here.
from book.models import Category, Book, Images, Comment
from home.models import Setting, ContactFormu, ContactFormMessage, UserProfile


def index(request):
    category = Category.objects.all()
    sliderdata = Book.objects.all()[:2]
    setting = Setting.objects.get(pk=1)
    lastbooks = Book.objects.all().order_by('-id')[:9]
    randombooks = Book.objects.all().order_by('?')[:6]
    randombooks2 = Book.objects.all()[:6]
    context = {
        'sliderdata':sliderdata,
        'page':'home',
        'setting': setting,
        'category': category,
        'lastbooks': lastbooks,
        'randombooks': randombooks,
        'randombooks2': randombooks2,
    }
    return render(request,'index.html',context)

def hakkimizda(request):
     category = Category.objects.all()
     setting = Setting.objects.get(pk=1)
     context = {
         'setting': setting,
         'page': hakkimizda,
         'category': category,
     }
     return render(request,'hakkimizda.html',context)

def iletisim(request):
    category = Category.objects.all()
    if request.method == 'POST':  # form post edildiyse
        form = ContactFormu(request.POST)
        if form.is_valid():
            data = ContactFormMessage()  # model ile bağlantı kur
            data.name = form.cleaned_data['name']  # formdan bilgiyi al
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()  # veritabanına kaydet
            messages.success(request, "Mesajınız başarı ile gönderilmiştir. Teşekkür Ederiz..")
            return HttpResponseRedirect('/iletisim')
    setting = Setting.objects.get(pk=1)
    form = ContactFormu()
    context = {'setting': setting, 'category': category, 'form': form}
    return render(request, 'iletisim.html', context)

def category_books(request,id,slug):
    category = Category.objects.all()
    books = Book.objects.filter(category_id=id)
    context = {'books': books,
               'category': category
               }
    return render(request,'book.html',context)


def books(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    books = Book.objects.all()
    context = {'setting': setting, 'category': category,  'books': books}
    return render(request, 'book.html', context)


def book_detail(request, id, slug):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    books = Book.objects.get(pk=id)
    images = Images.objects.filter(book_id=id)
    comments = Comment.objects.filter(book_id=id)
    context = {'books': books,
               'category': category,
               'images': images,
               'setting': setting,
               'comments': comments,

               }
    return render(request, 'book_detail.html', context)


def book_search(request):
    setting = Setting.objects.get(pk=1)
    if request.method == 'POST':  # Check form post
        form = SearchForm(request.POST)  # Get form data
        if form.is_valid():
            category = Category.objects.all()
            query = form.cleaned_data['query']  # Get form data
            catid = form.cleaned_data['catid']  # Get form data

            if catid == 0:
                books = Book.objects.filter(title__icontains=query)  # Select * from Book where title like %query%
            else:
                books = Book.objects.filter(title__icontains=query, category_id=catid)
            # return HttpResponse(Books)
            context = {'books': books,
                       'category': category,
                       'setting': setting,
                       }
            return render(request, 'book_search.html', context)
    return HttpResponseRedirect('/')

def book_search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        book = Book.objects.filter(title__icontains=q)
        results = []
        for rs in book:
            book_json = {}
            book_json = rs.title
            results.append(book_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)



def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


def login_view(request):
    setting = Setting.objects.get(pk=1)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return HttpResponseRedirect('/')
        else:
            messages.error(request, "Login Hatası ! Kullanıcı adı yada şifre yanlış")
            return HttpResponseRedirect('/login')
    category = Category.objects.all()
    context = {
        'category': category,
        'setting': setting,
               }
    return render(request, 'login.html', context)

def signup_view(request):
    setting = Setting.objects.get(pk=1)
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            login(request, user)
            current_user = request.user
            data = UserProfile()
            data.user_id = current_user.id
            data.image = 'images/users/user.png'
            data.save()
            messages.success(request, "Hoş geldiniz... Sitemize başarılı bir şekilde üye oldunuz. İyi alışverişler dileriz.")
            return HttpResponseRedirect('/')

    form = SignUpForm()
    category = Category.objects.all()
    context = {'category': category,
               'form': form,
               'setting': setting,
               }
    return render(request, 'signup.html', context)